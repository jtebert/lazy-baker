# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_auto_20170824_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipepage',
            name='notes',
            field=models.TextField(blank=True, help_text='Additional notes such as substitusions. This text will be formatted with markdown.'),
        ),
    ]
