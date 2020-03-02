import django
from django.db import models
from accounts.models import SellerFactory, SellerFactoryEmployee, Buyer
from django.contrib.auth.models import User
import datetime


class Auction(models.Model):
    factory = models.OneToOneField(SellerFactory, on_delete=models.CASCADE)
    employee = models.OneToOneField(SellerFactoryEmployee, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    tonnes = models.IntegerField()
    tonnes_left = models.IntegerField(null=True)
    price_per_tonne = models.IntegerField()
    date_harvested = models.DateField()
    COFFEE_TYPES = [("Arabica", "Arabica"), ("Robusta", "Robusta")]
    STATUS = [
        ("Washed", "Washed"),
        ("semi-washed", "semi-washed"),
        ("honey", "honey"),
        ("natural", "natural"),
    ]
    BEAN_SIZE = [("small", "small"), ("medium", "medium"), ("large", "large")]

    GRADES = [("Grade 1", "Grade 1"), ("Grade 2", "Grade 2"), ("Grade 3", "Grade 3")]
    grade = models.TextField(max_length=20, choices=GRADES, default="Grade 1")
    bean_size = models.CharField(max_length=20, choices=BEAN_SIZE, default="small")
    status = models.CharField(max_length=20, choices=STATUS, default="Washed")
    # Extras

    tempreture = models.CharField(max_length=12, default="0")
    description = models.TextField(default="")
    humidity = models.CharField(max_length=12, default="0")
    soil_ph = models.CharField(max_length=12, default="0")

    coffee_type = models.CharField(
        choices=COFFEE_TYPES, max_length=10, default="Arabica"
    )
    date_placed = models.DateTimeField(auto_now_add=True, null=True)
    verified = models.BooleanField(default=False)
    sold_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.factory.factory_name} auction"


class Order(models.Model):
    date_placed = models.DateTimeField(null=True, auto_now_add=True)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE)
    employee = models.ForeignKey(
        SellerFactoryEmployee, on_delete=models.CASCADE, default=None
    )
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    expected_date = models.DateTimeField(null=True, blank=True)
    amount = models.IntegerField()
    status = models.IntegerField(default=0)

    # Shipping Information
    shipping_address = models.TextField(null=True, blank=True)
    shipment_id = models.CharField(null=True, blank=True, max_length=20)
    vessel_number = models.CharField(default="", max_length=20)
    shipment_company = models.CharField(default="", max_length=20)
    estimated_time_on_ship = models.CharField(default="0", max_length=20)
    time_of_shipping = models.DateField(default="2020-01-01")
    shipment_handler_phone = models.CharField(default="", max_length=15)
    arrived = models.BooleanField(default=False)

    # BlockChain implementation
    chain = models.TextField(default="")
    chain_valid = models.BooleanField(default=False)
    order_hash = models.CharField(default="", max_length=200)
    when_arrived = models.DateTimeField(default=django.utils.timezone.now, null=True)
    last_order = models.BooleanField(default=False)

    def __str__(self):
        return f"order {self.id}"


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True)


class AdminMessage(models.Model):
    isglobal = models.BooleanField(default=False)
    reciever = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, default=None, blank=True, null=True
    )
    content = models.TextField()
    title = models.CharField(max_length=50)
    link = models.CharField(max_length=200, null=True, default="#")

    def __str__(self):
        return self.title
