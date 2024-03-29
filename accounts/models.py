from django.db import models
from django.contrib.auth.models import User as user_model

User = user_model


class SellerFactory(models.Model):
    date_created = models.DateField(auto_now_add=True, null=True)
    factory_name = models.CharField(max_length=30)
    factory_initials = models.CharField(max_length=10, null=True)

    company_email = models.EmailField()
    phone = models.CharField(max_length=20)
    region = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    street_name = models.CharField(max_length=40, default="", null=True)
    zip_code = models.CharField(max_length=20, default="", null=True)
    physical_address = models.CharField(max_length=40, default="", null=True)

    trade_license = models.FileField(null=True, blank=True)
    rating = models.IntegerField(null=True)
    factory_logo = models.ImageField(null=True)
    googlemap = models.TextField(null=True)
    factory_bio = models.TextField(default="No bio")
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.factory_name


class SellerFactoryEmployee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    factory = models.ForeignKey(
        SellerFactory, on_delete=models.CASCADE, null=False, blank=False
    )
    profile_picture = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    use_case = models.TextField(null = True)
    profile_picture = models.ImageField(blank=True, null=True)
    country = models.CharField(max_length = 20, null = True)
    phone = models.IntegerField(null = True)
    address = models.TextField(null = True)


    def __str__(self):
        return self.user.username


class HomepageSlides(models.Model):
    hq_image = models.ImageField(null=True)
    main_title = models.CharField(max_length=50, blank=True, null=True)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()

    def __str__(self):
        return self.main_title


class BestBlog(models.Model):
    hq_image = models.ImageField(null=True)
    main_title = models.CharField(max_length=50, blank=True, null=True)
    sub_title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    link = models.CharField(max_length=100)

    def __str__(self):
        return self.main_title
