from django.contrib import admin
from .models import (
    SellerFactory,
    Buyer,
    SellerFactoryEmployee,
    HomepageSlides,
    BestBlog,
)
from django.contrib.auth.models import User

# admin.site.register(User)
admin.site.register(SellerFactory)
admin.site.register(SellerFactoryEmployee)
admin.site.register(Buyer)
admin.site.register(HomepageSlides)
admin.site.register(BestBlog)
