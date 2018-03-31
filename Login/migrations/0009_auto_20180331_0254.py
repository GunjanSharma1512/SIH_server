# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-30 21:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0008_auto_20180331_0125'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='mse',
            field=models.DecimalField(decimal_places=40, default=0, max_digits=1000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='images',
            name='ocr',
            field=models.DecimalField(decimal_places=40, default=0, max_digits=1000),
            preserve_default=False,
        ),
    ]