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
                },
                format="yyyy-mm-dd",
            ),
        }


class CreateAuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            "tonnes",
            "price_per_tonne",
            "bean_size",
            "status",
            "coffee_type",
            "grade",
            "tempreture",
            "humidity",
            "soil_ph",
            "description",
        ]

        widgets = {
            "tonnes": forms.NumberInput(
                attrs={
                    "placeholder": ("Enter number of tonnes to auction"),
                    "class": "form-control slide-left-input",
                }
            ),
            "price_per_tonne": forms.NumberInput(
                attrs={
                    "placeholder": ("Enter Price per tonne to sell in USD"),
                    "class": "form-control slide-left-input",
                }
            ),
            "bean_size": forms.Select(
                choices=("small", "medium", "large"), attrs={"class": "form-control"}
            ),
            "coffee_type": forms.Select(
                choices=("Arabica", "Robusta"), attrs={"class": "form-control"}
            ),
            "grade": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(
                choices=("Washed", "semi-washed", "honey", "natural"),
                attrs={"class": "form-control"},
            ),
            "tempreture": forms.NumberInput(
                attrs={
                    "placeholder": (
                        "Enter Ambient tempreture of area where product was grown(optional)"
                    ),
                    "class": "form-control slide-left-input",
                }
            ),
            "humidity": forms.NumberInput(
                attrs={
                    "placeholder": ("Humidity or the area(optional)"),
                    "class": "form-control slide-left-input",
                }
            ),
            "soil_ph": forms.TextInput(
                attrs={
                    "placeholder": ("Area Soil PH(Optional)"),
                    "class": "form-control slide-left-input",
                    "helptext": "Enter a decimal number",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": ("Enter a description of the auction"),
                    "class": "form-control slide-left-input",
                }
            ),
        }
