# Generated by Django 3.0.2 on 2020-01-23 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_sellerfactory_factory_logo'),
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Transaction',
            new_name='Order',
        ),
    ]
