# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-05 09:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jctslapi', '0016_admin'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Admin',
            new_name='AdminUser',
        ),
    ]
