from django.contrib import admin
from .models import Escalation, RawFeedBack, Contact
# Register your models here.

admin.site.register(Escalation)
admin.site.register(RawFeedBack)
admin.site.register(Contact)