# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-28 06:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jctslapi', '0002_busroute_liveconductordetails'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='liveconductordetails',
            name='cid',
        ),
        migrations.AddField(
            model_name='liveconductordetails',
            name='cusername',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
