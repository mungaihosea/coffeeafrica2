# Generated by Django 3.0.2 on 2020-02-19 08:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0040_auto_20200219_0732'),
        ('feedback', '0003_rawfeedback_object_of_concern'),
    ]

    operations = [
        migrations.AlterField(
            model_name='escalation',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='transactions.Order'),
        ),
    ]
