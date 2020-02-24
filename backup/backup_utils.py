from .models import BackAuction, BackChat, BackOrder


def NewAuctionBackUp(auction_obj):
    backup = BackAuction(
        factory=auction_obj.factory,
        employee=auction_obj.employee,
        date=auction_obj.date,
        tonnes=auction_obj.tonnes,
        tonnes_left=auction_obj.tonnes_left,
        price_per_tonne=auction_obj.price_per_tonne,
        date_harvested=auction_obj.date_harvested,
        bean_size=auction_obj.bean_size,
        status=auction_obj.status,
        tempreture=auction_obj.tempreture,
        description=auction_obj.description,
        humidity=auction_obj.humidity,
        parent_id=auction_obj.pk,
        soil_ph=auction_obj.soil_ph,
        coffee_type=auction_obj.coffee_type,
        date_placed=auction_obj.date_placed,
        verified=auction_obj.verified,
    )

    backup.save()


def UpdateBackUpAuction(auction_obj):
    backups = BackAuction.objects.all()
    for b in backups:
        if b.factory == auction_obj.factory and b.parent_id == auction_obj.pk:
            backup = b
            print(b)
            break

    backup.factory = auction_obj.factory
    backup.employee = auction_obj.employee
    backup.date = auction_obj.date
    backup.tonnes = auction_obj.tonnes
    backup.tonnes_left = auction_obj.tonnes_left
    backup.price_per_tonne = auction_obj.price_per_tonne
    backup.date_harvested = auction_obj.date_harvested
    backup.bean_size = auction_obj.bean_size
    backup.status = auction_obj.status
    backup.tempreture = auction_obj.tempreture
    backup.description = auction_obj.description
    backup.humidity = auction_obj.humidity
    backup.soil_ph = auction_obj.soil_ph
    backup.coffee_type = auction_obj.coffee_type
    backup.date_placed = auction_obj.date_placed
    backup.verified = auction_obj.verified
    backup.save()


def NewOrderBackUp(order_obj):
    auctionsback = BackAuction.objects.all()
    for auct in auctionsback:
        if auct.parent_id == order_obj.auction.pk:
            auction = auct
    order = BackOrder(
        date_placed=order_obj.date_placed,
        buyer=order_obj.buyer,
        employee=order_obj.employee,
        auction=auction,
        expected_date=order_obj.expected_date,
        amount=order_obj.amount,
        status=order_obj.status,
        shipping_address=order_obj.shipping_address,
        estimated_time_on_ship=order_obj.estimated_time_on_ship,
        shipment_id=order_obj.shipment_id,
        vessel_number=order_obj.vessel_number,
        shipment_company=order_obj.shipment_company,
        shipment_handler_phone=order_obj.shipment_handler_phone,
        arrived=order_obj.arrived,
        chain=order_obj.chain,
        chain_valid=order_obj.chain_valid,
        order_hash=order_obj.order_hash,
    )

    order.save()


def UpdateBackUpOrder(order_obj):
    order = BackOrder.objects.get(date_placed=order_obj.date_placed)
    order.date_placed = order_obj.date_placed
    order.buyer = order_obj.buyer
    order.employee = order_obj.employee
    order.expected_date = order_obj.expected_date
    order.amount = order_obj.amount
    order.status = order_obj.status
    order.shipping_address = order_obj.shipping_address
    order.estimated_time_on_ship = order_obj.estimated_time_on_ship
    order.shipment_id = order_obj.shipment_id
    order.vessel_number = order_obj.vessel_number
    order.shipment_company = order_obj.shipment_company
    order.shipment_handler_phone = order_obj.shipment_handler_phone
    order.arrived = order_obj.arrived
    order.chain = order_obj.chain
    order.chain_valid = order_obj.chain_valid
    order.oder_hash = order_obj.order_hash

    order.save()

