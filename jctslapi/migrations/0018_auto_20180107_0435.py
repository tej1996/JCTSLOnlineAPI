# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-07 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jctslapi', '0017_auto_20180105_0943'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickettransactionscond',
            name='datetime',
            field=models.DateTimeField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='tickettransactionscond',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
        migrations.AddField(
            model_name='tickettransactionsuser',
            name='status',
            field=models.CharField(default='active', max_length=20),
        ),
    ]
