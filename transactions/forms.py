from django.forms import ModelForm
import django.forms as forms
from django import forms as Nforms
from .models import Order, Auction
from django.db import models as db_models
from django.contrib.admin.widgets import AdminDateWidget


class ShipmentInfoForm(ModelForm):
    class Meta:
        model = Order
        fields = [
            "shipment_id",
            "vessel_number",
            "shipment_company",
            "estimated_time_on_ship",
            "time_of_shipping",
            "shipment_handler_phone",
        ]

        widgets = {
            "shipment_id": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Shipment ID"}
            ),
            "shipment_company": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Shipment Company name",
                }
            ),
            "vessel_number": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Enter Vessel Number"}
            ),
            "estimated_time_on_ship": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Estimated Time on ship",
                }
            ),
            "shipment_handler_phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Phone"}
            ),
            "time_of_shipping": AdminDateWidget(
                attrs={
                    "placeholder": ("enter Date e.g 1999-1-4 yyyy-mm-dd"),
                    "class": "form-control",
                }
            ),
        }


class CreateAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            "tonnes",
            "price_per_tonne",
            "date_harvested",
            "bean_size",
            "status",
            "tempreture",
            "humidity",
            "soil_ph",
            "description",
        ]

        widgets = [[]]
