# Generated by Django 3.0.2 on 2020-01-23 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_sellerfactory_rating'),
    ]

    operations = [
        migrations.AddField(
            model_name='sellerfactory',
            name='factory_logo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
