# Generated by Django 2.0 on 2018-06-12 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0011_auto_20180612_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='posted_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 12, 18, 18, 5, 60988)),
        ),
    ]
