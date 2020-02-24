# Generated by Django 3.0.2 on 2020-02-19 05:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0035_adminmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminmessage',
            name='isglobal',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='adminmessage',
            name='reciever',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
