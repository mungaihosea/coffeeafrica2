from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Auction, Order, Chat, AdminMessage
from backup.models import BackAuction, BackOrder
from backup import backup_utils
import calendar
import dateutil
from . import calenderutil

try:
    from ..blockSys import intergrator
except:
    from blockSys import intergrator, utils
import django
from accounts.models import SellerFactory
from accounts.models import SellerFactoryEmployee
from accounts.models import Buyer
from blockSys import *
from hashlib import sha256
from . import forms
from django.views.generic import View
from django.contrib.auth.models import User
import datetime
import time
from .forms import CreateAuctionForm
import json


def add_auction(request):
    form = CreateAuctionForm()
    # if request.method == 'POST':
    #     if request.POST['pass']:
    #         print('password came in')
    #         return render(request, 'add_auction.html')
    # return render(request, 'confirm_password.html', {})
    return render(request, "add_auction.html", context={"form": form})


def confirmArival(request, order_id):
    print(request.GET.keys())
    # order = Order.objects.get(pk=order_id)
    # order.arrived = True
    # order.status = 3
    # order.when_arrived = django.utils.timezone.now
    # chain = intergrator.ReadChainFromFile(order_id)
    # chain.addTochain(order)

    # order.chain = chain.blockchain.getChainList()
    # hasher = sha256(str(order.chain).encode("utf-8"))

    # order.hash = hasher.hexdigest()
    # order.chain_valid = chain.CheckValidity()
    # order.save()
    # chain.DumpChain(order_id)
    # backup_utils.BackOrder(order)
    # if order.last_order:
    #     order.auction.delete()
    # return HttpResponse("Updated")


class GetBuyerChartView(View):
    def get(self, request, buyer_name, *args, **kwargs):
        print(buyer_name)
        try:
            buyer = Buyer.objects.get(user=User.objects.get(username=buyer_name))
            auctions = BackAuction.objects.all()
            prices = []
            months_price = []
            months = []
            for auction in auctions:
                price = auction.price_per_tonne
                months_price.append(auction.date)
                prices.append(price)
            sumprice = sum(prices)
            months = calenderutil.getAllMonthsStr()
            mean_price = sumprice / len(prices)
            context = {
                "prices": prices,
                "months_price": months_price,
                "months": months,
                "MeanPrice": round(mean_price, 3),
            }

            factories_traded = []
            amount = []
            amts = {}
            orders = BackOrder.objects.filter(buyer=buyer)
            for order in orders:
                factory = order.employee.factory
                if factory not in factories_traded:
                    factories_traded.append(factory)
                if amts.get(factory.factory_name):
                    amts[factory.factory_name] = (
                        order.amount + amts[factory.factory_name]
                    )
                else:
                    amts[factory.factory_name] = order.amount

            for x in range(len(factories_traded)):
                amount.append(amts.get(factories_traded[x].factory_name))

            context["factories"] = factories_traded
            print(amount)
            context["amounts"] = amount

            return render(request, "buyer_charts.html", context)
        except:
            auctions = Auction.objects.all()
            prices = []
            months_price = []
            months = []
            for auction in auctions:
                price = auction.price_per_tonne
                months_price.append(auction.date)
                prices.append(price)
            sumprice = sum(prices)
            months = calenderutil.getAllMonthsStr()
            try:
                mean_price = sumprice / len(prices)
            except:
                mean_price = 0
            context = {
                "prices": prices,
                "months_price": months_price,
                "months": months,
                "MeanPrice": round(mean_price, 3),
            }

            return render(request, "buyer_charts.html", context)


class GetChartView(View):
    def get(self, request, factory_name):
        factory = SellerFactory.objects.get(factory_name=factory_name)

        class Stat:
            def __init__(self, data, year=2019):
                self.data = data
                self.year = year

        orders = BackOrder.objects.all()
        data = {
            "jan": 0,
            "feb": 0,
            "mar": 0,
            "apr": 0,
            "may": 0,
            "jun": 0,
            "jul": 0,
            "aug": 0,
            "sep": 0,
            "oct": 0,
            "nov": 0,
            "dec": 0,
        }
        processed_orders = 0
        received = 0
        total_tonnes = 0
        tones_sold = 0

        auctions = BackAuction.objects.all()
        for auction in auctions:
            if auction.factory == factory:
                total_tonnes += auction.tonnes
                tones_sold += auction.tonnes - auction.tonnes_left

        for order in orders:
            if order.auction.factory == factory:
                if order.status == 2 or order.status == 3:
                    processed_orders += 1
                if order.auction.factory == factory:
                    received += 1
                if order.arrived:
                    if order.date_placed.year == datetime.date.today().year:
                        if order.date_placed.month == 1:
                            data["jan"] += order.amount
                        elif order.date_placed.month == 2:
                            data["feb"] += order.amount
                        elif order.date_placed.month == 3:
                            data["mar"] += order.amount
                        elif order.date_placed.month == 4:
                            data["apr"] += order.amount
                        elif order.date_placed.month == 5:
                            data["may"] += order.amount
                        elif order.date_placed.month == 6:
                            data["jun"] += order.amount
                        elif order.date_placed.month == 7:
                            data["jul"] += order.amount
                        elif order.date_placed.month == 8:
                            data["aug"] += order.amount
                        elif order.date_placed.month == 9:
                            data["sep"] += order.amount
                        elif order.date_placed.month == 10:
                            data["oct"] += order.amount
                        elif order.date_placed.month == 12:
                            data["nov"] += order.amount
                        elif order.date_placed.month == 12:
                            data["dec"] += order.amount

        value_increase = 0
        if datetime.date.today().month == 1:
            val = data.get("jan")
            value_increase = val
        elif datetime.date.today().month == 2:
            val = data.get("feb")
            value_increase = val - data.get("jan")
        elif datetime.date.today().month == 3:
            val = data.get("mar")
            value_increase = val - data.get("feb")
        elif datetime.date.today().month == 4:
            val = data.get("apr")
            value_increase = val - data.get("mar")
        elif datetime.date.today().month == 5:
            val = data.get("may")
            value_increase = val - data.get("apr")
        elif datetime.date.today().month == 6:
            val = data.get("jun")
            value_increase = val - data.get("may")
        elif datetime.date.today().month == 7:
            val = data.get("jul")
            value_increase = val - data.get("jun")
        elif datetime.date.today().month == 8:
            val = data.get("aug")
            value_increase = val - data.get("jun")
        elif datetime.date.today().month == 9:
            val = data.get("sep")
            value_increase = val - data.get("aug")
        elif datetime.date.today().month == 10:
            val = data.get("oct")
            value_increase = val - data.get("sep")
        elif datetime.date.today().month == 12:
            val = data.get("nov")
            value_increase = val - data.get("oct")
        elif datetime.date.today().month == 12:
            val = data.get("dec")
            value_increase = val - data.get("nov")

        stat = Stat(data, datetime.date.today().year)
        context = {}
        context["stat"] = stat
        context["processed"] = processed_orders
        context["recieved"] = received
        context["total_tonnes"] = total_tonnes
        context["tonnes_sold"] = tones_sold

        if value_increase < 0:
            value_increase = str(value_increase)
        elif value_increase == 0:
            value_increase = str(value_increase)
        else:
            value_increase = "+" + str(value_increase)

        context["value_increase"] = value_increase

        percentage_sold = 0.00
        if total_tonnes != 0:
            percentage_sold = (tones_sold * 100) / total_tonnes

        context["percentage_sold"] = round(percentage_sold, 2)

        return render(request, "factory_charts.html", context)


class AcceptOrderView(View):
    def post(self, request, factory_id):
        id = request.POST.get("id")
        order = Order.objects.get(pk=id)
        order.status = 1
        chain = intergrator.ReadChainFromFile(id)
        chain.addTochain(order)
        order.order_valid = chain.CheckValidity()
        order.chain = chain.blockchain.getChainList()
        chain.DumpChain(id)
        myhasher = sha256(str(order.chain).encode("utf-8"))
        order.hash = myhasher.hexdigest()
        order.save()
        backup_utils.UpdateBackUpOrder(order)
        return HttpResponse("Successfully Updated")


class DeletAuction(View):
    def get(self, request, auction_id):
        print(auction_id)
        auction = Auction.objects.get(pk=auction_id)
        try:
            auction.delete()
            return HttpResponse("Removed")
        except:
            print("Error")
            auction.delete()
            return HttpResponse("Error")


class CreateAuction(View):
    def post(self, request, *args, **kwargs):
        # creating auction,
        try:
            auction = Auction(
                factory=SellerFactory.objects.get(pk=request.POST.get("factory")),
                employee=SellerFactoryEmployee.objects.get(
                    pk=request.POST.get("employee")
                ),
                tonnes=request.POST.get("tonnes"),
                price_per_tonne=request.POST.get("price_per_tonne"),
                date_harvested=request.POST.get("date_harvested"),
                bean_size=request.POST.get("bean_size"),
                status=request.POST.get("status"),
                tonnes_left=request.POST.get("tonnes"),
                tempreture=request.POST.get("tempreture"),
                humidity=request.POST.get("humidity"),
                soil_ph=request.POST.get("soil_ph"),
                description=request.POST.get("description"),
                verified=False,
            )
            auction.save()
            backup_utils.NewAuctionBackUp(auction)
            return redirect("/dashboard/")
        except:
            return render(request, "add_auction.html", context={"errors": "Invalid"})


class EnterShipmentInfoView(View):
    def get(self, request, order_id):
        order = Order.objects.get(pk=order_id)
        form = forms.ShipmentInfoForm()
        return render(request, "shipmentForm.html", {"form": form, "order": order})

    def post(self, request):
        order = Order.objects.get(pk=request.POST.get("id"))
        try:
            order.shipment_id = request.POST.get("shipment_id")
            order.vessel_number = request.POST.get("vessel_number")
            order.shipment_company = request.POST.get("shipment_company")
            order.estimated_time_on_ship = request.POST.get("estimated_time_on_ship")
            order.shipment_handler_phone = request.POST.get("shipment_handler_phone")
            order.time_of_shipping = request.POST.get("time_of_shipping")
            order.status = 3
            chain = intergrator.ReadChainFromFile(request.POST.get("id"))
            chain.addTochain(order)
            order.chain = chain.blockchain.getChainList()
            order.chain_valid = chain.CheckValidity()
            hasher = sha256(str(order.chain).encode("utf-8"))
            order.order_hash = hasher.hexdigest()
            order.save()
            backup_utils.UpdateBackUpOrder(order)
            chain.DumpChain(order.pk)
            return HttpResponse("SuccessFully Updated!")
        except:
            return HttpResponse("Error When updating!")


class AddShipmentAddressView(View):
    def post(self, request, *args, **kwargs):
        print("wtf")
        id = request.POST.get("id")
        print(id)
        order = get_object_or_404(Order, pk=id)
        shipmentinfo = f"ZipCode: {request.POST.get('zip')}     Town: {request.POST.get('town')}    Address: {request.POST.get('address')}"
        order.shipping_address = shipmentinfo
        order.save()
        backup_utils.UpdateBackUpOrder(order)
        return HttpResponse("Shipment Details Added!")


class ETime:
    def __init__(self, time, order, late, lateby, other=None):
        self.time = time
        self.late = late
        self.late_by = lateby
        self.order = order
        self.other = other


def view_market(request):
    auction_queryset = Auction.objects.filter(sold_out=False)
    orders = []
    for auction in auction_queryset:
        ordermatch = Order.objects.filter(auction=auction)
        orders.append(ordermatch)
    time_remaining = []
    for ordermatches in orders:
        for order in ordermatches:
            order.time_of_shipping = datetime.datetime(
                year=order.time_of_shipping.year,
                month=order.time_of_shipping.month,
                day=order.time_of_shipping.day,
            )
            order.save()
            current_time = datetime.date.today()
            time_ship = order.time_of_shipping
            time_ship = datetime.date(time_ship.year, time_ship.month, time_ship.day)
            add = False
            days1 = 0
            if time_ship.month != current_time.month:
                days1 = calendar.monthrange(time_ship.year, time_ship.month)
                add = True

            elapsed_time = current_time.day - time_ship.day
            if add:
                elapsed_time += days1[1]

            elapsed_time_save = elapsed_time
            elapsed_time = elapsed_time
            # elapsed_time = elapsed_time.day
            expected_to_arrive = time_ship + datetime.timedelta(
                hours=int(order.estimated_time_on_ship)
            )
            lateby = elapsed_time - expected_to_arrive.day

            cash = order.amount * order.auction.price_per_tonne

            late = False
            if lateby > 0:
                late = True
            E = ETime(elapsed_time, order, late, lateby, cash)

            time_remaining.append(E)

    context = {
        "auction_queryset": auction_queryset,
        "orders": orders,
        "Etimes": time_remaining,
    }
    return render(request, "view_market.html", context)


def view_factory(request, factory_id):
    factory = get_object_or_404(SellerFactory, id=factory_id)
    auctions = Auction.objects.filter(factory=factory)
    context = {
        "factory": factory,
        "auctions": auctions,
    }
    return render(request, "view_factory.html", context)


def view_market_id(request, id):
    auction = get_object_or_404(Auction, id=id)

    context = {
        "auction": auction,
    }
    return render(request, "buy_bundle.html", context)


def view_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    chat_queryset = Chat.objects.filter(order=order)
    context = {"chat_queryset": chat_queryset, "order": order, "user": request.user}
    return render(request, "view_order.html", context)


def view_auction(request):
    auction = request.user.sellerfactoryemployee.factory.auction
    order_queryset = Order.objects.filter(auction=auction)
    context = {
        "auction": auction,
        "order_queryset": order_queryset,
    }
    return render(request, "current_auction.html", context)


def chat(request):
    context = {}
    return render(request, "chat.html", context)


class ShowAuctionHistory(View):
    def get(self, request, factory_name, *args, **kwargs):
        auctions = BackAuction.objects.filter(
            factory=SellerFactory.objects.get(factory_name=factory_name)
        )
        context = {"auctions": auctions}
        return render(request, "auction_history.html", context)


class ShowTransactions(View):
    def get(self, request, factory_name, *args, **kwargs):
        try:
            factorys = SellerFactory.objects.all()
            transactions = []
            auctionss = BackAuction.objects.filter(
                factory=SellerFactory.objects.get(factory_name=factory_name)
            )
            for factory in factorys:
                for auction in auctionss:
                    transactionsof = BackOrder.objects.filter(auction=auction,)
                    for y in transactionsof:
                        transactions.append(y)
            hold = []
            n = len(transactions)
            x = n - 1
            while x >= 0:
                hold.append(transactions[x])
                x -= 1
            transactions = hold
            context = {"transactions": transactions}
            print(transactions)
            return render(request, "transactions.html", context)
        except:
            buyer = Buyer.objects.get(user=User.objects.get(username=factory_name))
            transactions = BackOrder.objects.filter(buyer=buyer)
            hold = []
            n = len(transactions)
            x = n - 1
            while x >= 0:
                hold.append(transactions[x])
                x -= 1
            transactions = hold
            context = {"transactions": transactions}
            print(transactions)
            return render(request, "transactions.html", context)


class ShowNotifications(View):
    def get(self, request, name, *args, **kwargs):
        try:
            buyer = Buyer.objects.get(user=User.objects.get(username=name))
            order_queryset = Order.objects.filter(buyer=buyer)
            auctions = []
            for order in order_queryset:
                auction = order.auction
                if auction not in auctions:
                    auctions.append(auction)
            notifications = []
            for order in order_queryset:
                if order.status == 1 and not order.shipping_address:
                    notification = Notification(
                        1,
                        "view_order",
                        f"Your Order for the {order.auction} has been accepted",
                        order.id,
                        "transactions",
                    )
                elif order.status == 2 and order.shipment_company:
                    notification = Notification(
                        1,
                        "view_order",
                        f"Your Order for the {order.auction} is on ship. Click to check shipment details",
                        order.id,
                        "transactions",
                    )
                elif order.status == 2 and not order.shipment_company:
                    notification = Notification(
                        1,
                        "view_order",
                        f"Your Order for the {order.auction} is being processed",
                        order.id,
                        "transactions",
                    )
                elif order.status == 3 and not order.arrived:
                    notification = Notification(
                        1,
                        "view_order",
                        f"Your Order for the {order.auction} is has been processed, click to view details",
                        order.id,
                        "transactions",
                    )
                elif order.arrived:
                    notification = Notification(
                        1,
                        "view_order",
                        f"Order {order.pk} for auction {order.auction.pk} by '{order.auction.factory.factory_name}' has verified arrival, thank you for trading on our platform",
                        order.id,
                        "transactions",
                    )
            try:
                notifications.append(notification)
            except:
                notifications = []
            context = {
                "notifications": notifications,
                "auctions": auctions,
                "orders": order_queryset,
            }

            global_admin_messages = AdminMessage.objects.filter(isglobal=True)
            admin_to_user_messages = AdminMessage.objects.filter(
                reciever=User.objects.get(username=name)
            )
            context["admin_messages"] = global_admin_messages
            context["admin_to_me"] = admin_to_user_messages
            return render(request, "notifications.html", context)
        except:
            employee = SellerFactoryEmployee.objects.get(
                user=User.objects.get(username=name)
            )
            factory = employee.factory
            try:
                order_queryset = Order.objects.filter(
                    auction=Auction.objects.get(factory=factory)
                )
            except:
                order_queryset = []
            auctions = []
            notifications = []
            for order in order_queryset:
                auction = order.auction
                if auction not in auctions:
                    auctions.append(auction)
            for order in order_queryset:
                if order.status == 0:
                    notification = Notification(
                        1,
                        "view_order",
                        f"You have a new order for your auction by {order.buyer}: {order.amount} Tonne(s), {order.date_placed}",
                        order.id,
                        "transactions",
                    )
                elif order.shipping_address and not order.shipment_company:
                    notification = Notification(
                        1,
                        "view_order",
                        f"{order.buyer} has filled shipping addresses for Order {order.auction} click to check.",
                        order.id,
                        "transactions",
                    )
                elif order.status == 3 and not order.arrived:
                    notification = Notification(
                        1,
                        "view_order",
                        f"{order.pk} is on ship, we will notify you when the client confirms its arrival {datetime.datetime.today}",
                        order.id,
                        "transactions",
                    )
                elif order.arrived:
                    notification = Notification(
                        1,
                        "view_order",
                        f"Order {order.pk} for auction {order.auction.pk} has verified arrival, thank you for trading on our platform",
                        order.id,
                        "transactions",
                    )
            try:
                notifications.append(notification)
            except:
                notifications = []
            context = {
                "notifications": notifications,
                "auctions": auctions,
                "orders": order_queryset,
            }
            global_admin_messages = AdminMessage.objects.filter(isglobal=True)
            admin_to_user_messages = AdminMessage.objects.filter(
                reciever=User.objects.get(username=name)
            )
            context["admin_messages"] = global_admin_messages
            context["admin_to_me"] = admin_to_user_messages
            return render(request, "notifications.html", context)


class Notification:
    def __init__(self, type, action, messsage, id, app_name):
        self.type = type
        self.action = action
        self.message = messsage
        self.id = id
        self.app_name = app_name
