from django.urls import re_path, path
from .consumers import AuctionConsumer, ChatConsumer, NotificationConsumer, orderConsumer

websocket_urlpatterns = [
    # re_path(r'ws/transactions/addauction\$', AuctionConsumer)
    path('ws/transactions/addauction/', AuctionConsumer),
    path('ws/transactions/addorder/<str:employee_id>/', orderConsumer),
    path('ws/transactions/vieworder/<str:order_id>/', ChatConsumer),
    path('ws/transactions/notifications/<str:employee_id>/', NotificationConsumer)
]
