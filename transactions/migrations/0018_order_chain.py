# Generated by Django 3.0.2 on 2020-02-01 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0017_auto_20200130_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='chain',
            field=models.TextField(default=''),
        ),
    ]
