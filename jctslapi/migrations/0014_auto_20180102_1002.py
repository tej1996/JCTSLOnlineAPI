# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-02 10:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jctslapi', '0013_auto_20180102_0945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tickettransactionsuser',
            old_name='user_username',
            new_name='passen_email',
        ),
    ]
