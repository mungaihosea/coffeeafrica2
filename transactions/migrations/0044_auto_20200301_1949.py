# Generated by Django 3.0.3 on 2020-03-01 19:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('transactions', '0043_auto_20200301_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminmessage',
            name='reciever',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]
