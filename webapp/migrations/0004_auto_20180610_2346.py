# Generated by Django 2.0 on 2018-06-10 18:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_blogpost_posted_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='posted_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 10, 23, 46, 21, 416585)),
        ),
    ]
