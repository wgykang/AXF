# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-03 15:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APP', '0004_auto_20180703_1510'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainshow',
            old_name='prodectid2',
            new_name='productid2',
        ),
        migrations.RenameField(
            model_name='mainshow',
            old_name='prodectid3',
            new_name='productid3',
        ),
    ]
