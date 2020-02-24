from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.views.generic import View
from .models import RawFeedBack, Escalation
from django.contrib.auth.models import User
from transactions.models import Order

# Create your views here.


class CreateRawFeedBack(View):
    def post(self, request, *args, **kwargs):
        print(request.POST.keys())
        try:
            feebackObj = RawFeedBack(
                sender=User.objects.get(pk=request.POST.get("user")),
                object_of_concern=request.POST.get("obj"),
                message=request.POST.get("message"),
            )
            feebackObj.save()
            return HttpResponse("Feedback Sent, we value your feeback!")
        except:
            return HttpResponse("An error occured when uploading feedback")


class CreateEscalation(View):
    def post(self, request, *args, **kwargs):
        print(request.POST.get("user"))
        try:
            escalationObj = Escalation(
                sender=User.objects.get(pk=request.POST.get("user")),
                order=Order.objects.get(pk=request.POST.get("order")),
                comment=request.POST.get("message"),
                type=request.POST.get("type"),
            )
            escalationObj.save()
            return HttpResponse("Feedback Sent!")
        except:
            escalationObj = Escalation(
                sender=User.objects.get(pk=request.POST.get("user")),
                order=Order.objects.get(pk=request.POST.get("order")),
                comment=request.POST.get("message"),
                type=request.POST.get("type"),
            )
            return HttpResponse("An error occured when uploading feedback")


class MainFeedBackView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "feedback.html")
