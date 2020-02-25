# Generated by Django 3.0.3 on 2020-02-25 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_bestblog'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyer',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='sellerfactory',
            name='active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sellerfactory',
            name='factory_initials',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='sellerfactory',
            name='physical_address',
            field=models.CharField(default='', max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='sellerfactory',
            name='street_name',
            field=models.CharField(default='', max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='sellerfactory',
            name='zip_code',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='sellerfactoryemployee',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
