# Generated by Django 2.0 on 2018-06-10 18:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20180610_2346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productcategory',
            name='store_cats',
        ),
        migrations.AddField(
            model_name='productcategory',
            name='stores',
            field=models.ManyToManyField(blank=True, null=True, related_name='categories', to='webapp.Store'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='posted_on',
            field=models.DateTimeField(default=datetime.datetime(2018, 6, 11, 0, 26, 34, 909195)),
        ),
    ]
