# Generated by Django 3.0.2 on 2020-02-19 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0037_auction_sold_out'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='last_order',
            field=models.BooleanField(default=False),
        ),
    ]
