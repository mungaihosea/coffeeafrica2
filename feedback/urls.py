from django.urls import path
from .views import CreateEscalation, CreateRawFeedBack, MainFeedBackView

app_name = "feedback"

urlpatterns = [
    path("", CreateRawFeedBack.as_view(), name="createfeedback"),
    path("<int:order_id>/", CreateEscalation.as_view(), name="createescalation"),
    path("main/", MainFeedBackView.as_view(), name="showfeedback"),
]
