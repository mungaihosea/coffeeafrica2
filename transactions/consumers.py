from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
import json
from .models import Order, Auction, Chat
from django.shortcuts import get_object_or_404
from accounts.models import SellerFactoryEmployee
from django.contrib.auth.models import User
from blockSys import intergrator
from hashlib import sha256
from backup import backup_utils


class AuctionConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = "auction"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "message_received", "data": data}
        )

    def message_received(self, event):
        self.send(json.dumps(event["data"]))


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        chat_id = self.scope["url_route"]["kwargs"]["order_id"]
        print(chat_id)
        self.room_group_name = chat_id
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        received_data = json.loads(text_data)
        user = get_object_or_404(User, id=received_data["user"])
        order = get_object_or_404(Order, id=received_data["order_id"])
        Chat.objects.create(sender=user, content=received_data["content"], order=order)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "message_received", "data": json.loads(text_data)},
        )

    def message_received(self, event):
        self.send(json.dumps(event["data"]))


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["employee_id"]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )

        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer)(self.room_group_name, self.channel_name)

    def receive(self, text_data):
        print(json.loads(text_data))
        data = json.loads(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "notification_received", "data": data}
        )

    def notification_received(self, event):
        self.send(json.dumps(event["data"]))


class orderConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = self.scope["url_route"]["kwargs"]["employee_id"]
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name, self.channel_name
        )
        self.accept()

    def disconnect(self, code):
        async_to_sync(self.channel_layer)(self.room_group_name, self.channel_layer)

    def receive(self, text_data):
        print(self.room_group_name)
        wkstr = "[" + text_data + "]"
        wkstr = json.loads(wkstr)
        wkstr = wkstr[0]
        data = wkstr
        print(type(data), data)
        user_id = data["user"]
        print(user_id)
        employee = get_object_or_404(SellerFactoryEmployee, id=user_id)

        order = json.loads(text_data)
        auction = get_object_or_404(Auction, id=order["auction"])
        auction.tonnes_left = int(auction.tonnes_left) - int(order["tonnes"])
        last = False
        if auction.tonnes_left <= 0:
            auction.sold_out = True
            last = True
        auction.save()
        backup_utils.UpdateBackUpAuction(auction)
        order = Order.objects.create(
            buyer=self.scope["user"].buyer,
            employee=employee,
            auction=auction,
            expected_date=order["shipmentdate"],
            amount=order["tonnes"],
        )
        if last:
            order.last_order = True
        chain = intergrator.Chain_Model()
        chain.addTochain(order)
        order.chain = chain.blockchain.getChainList()
        order.chain_valid = chain.CheckValidity()
        order.save()
        hasher = sha256(str(order.chain).encode("utf-8"))
        hashout = hasher.hexdigest()
        order.order_hash = hashout
        order.save()
        backup_utils.NewOrderBackUp(order)

        chain.DumpChain(order.pk)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {"type": "order_received", "data": json.loads(text_data)},
        )

    def order_received(self, event):
        self.send(json.dumps(event["data"]))


# order = Order.objects.create(buyer = self.scope['user'].buyer,employee=employee, auction = auction, expected_date = order['date'], amount= order['amount'])
#         chain = intergrator.Chain_Model()
#         chain.addTochain(order)
#         print(chain)
#         chain.DumpChain(order.pk)
#         valid = chain.CheckValidity()
