from django.db import models
from django.contrib.auth.models import User
from transactions.models import Order

# Create your models here.
class RawFeedBack(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    object_of_concern = models.CharField(max_length=20, default="None")
    message = models.TextField()
    time_stamp = models.DateTimeField(auto_now_add=True)


class Escalation(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()
    TYPES = [
        ("clarification", "calrification"),
        ("Request", "Request"),
        ("Other", "Other"),
        ("Question", "Question"),
    ]
    type = models.CharField(max_length=20, choices=TYPES)

    def __str__(self):
        return "concerning " + self.order.__str__()
