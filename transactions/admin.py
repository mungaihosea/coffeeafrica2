from django.contrib import admin
from .models import Auction, Order, Chat, AdminMessage

admin.site.register(Auction)
admin.site.register(Order)
admin.site.register(Chat)
admin.site.register(AdminMessage)
