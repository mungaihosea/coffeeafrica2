# Generated by Django 3.0.2 on 2020-02-21 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_auto_20200219_1555'),
    ]

    operations = [
        migrations.CreateModel(
            name='BestBlog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hq_image', models.ImageField(null=True, upload_to='')),
                ('main_title', models.CharField(blank=True, max_length=50, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=100, null=True)),
                ('content', models.TextField()),
                ('link', models.CharField(max_length=100)),
            ],
        ),
    ]
