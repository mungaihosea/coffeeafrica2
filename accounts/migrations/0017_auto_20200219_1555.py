# Generated by Django 3.0.2 on 2020-02-19 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_homepageslides'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homepageslides',
            name='main_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='homepageslides',
            name='sub_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
