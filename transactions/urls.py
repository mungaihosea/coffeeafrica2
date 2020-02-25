from django.urls import path
from .views import (
    add_auction,
    view_market,
    view_market_id,
    view_order,
    view_auction,
    chat,
    view_factory,
    AcceptOrderView,
    EnterShipmentInfoView,
    AddShipmentAddressView,
    GetChartView,
    confirmArival,
    DeletAuction,
    CreateAuction,
    GetBuyerChartView,
    ShowAuctionHistory,
    ShowTransactions,
    ShowNotifications,
    pdf,
)

namespace = "transactions"

urlpatterns = [
    path("add_auction/", add_auction, name="add_auction"),
    path("view_market/", view_market, name="view_market"),
    path("view_market/<int:id>/", view_market_id, name="view_market"),
    path("view_order/<int:order_id>/", view_order, name="view_order"),
    path("view_auction/", view_auction, name="view_auction"),
    path("chat/", chat, name="chat"),
    path(
        "view_market/view_factory/<int:factory_id>/", view_factory, name="view_factory"
    ),
    path(
        "view_order/<int:factory_id>/update_order/",
        AcceptOrderView.as_view(),
        name="accept_order",
    ),
    path(
        "shipmentinfo/<int:order_id>/",
        EnterShipmentInfoView.as_view(),
        name="shipmentview",
    ),
    path("ShipmentSaved/", EnterShipmentInfoView.as_view(), name="saveshipment"),
    path(
        "ShipmentAddress/",
        AddShipmentAddressView.as_view(),
        name="addshippmentaddress",
    ),
    path("charts/<str:factory_name>", GetChartView.as_view(), name="charts"),
    path("bcharts/<str:buyer_name>", GetBuyerChartView.as_view(), name="bcharts"),
    path("order-arrived/<int:order_id>", confirmArival, name="confirm"),
    path(
        "auction-remove/<int:auction_id>", DeletAuction.as_view(), name="delete-auction"
    ),
    path("create_auction/", CreateAuction.as_view(), name="create_auction"),
    path(
        "auction_history/<str:factory_name>/",
        ShowAuctionHistory.as_view(),
        name="auction_history",
    ),
    path("<str:factory_name>/", ShowTransactions.as_view(), name="showtransactions",),
    path(
        "notifications/<str:name>/",
        ShowNotifications.as_view(),
        name="shownotifications",
    ),
    path('pdf/<str:factory_name>/', pdf, name='pdf')
]
