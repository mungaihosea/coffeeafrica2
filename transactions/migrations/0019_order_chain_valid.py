# Generated by Django 3.0.2 on 2020-02-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0018_order_chain'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='chain_valid',
            field=models.BooleanField(default=False),
        ),
    ]
