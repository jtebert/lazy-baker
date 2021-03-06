# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-23 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0010_categorygrouppage_icon'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipepage',
            name='servings',
        ),
        migrations.AddField(
            model_name='recipepage',
            name='recipe_yield',
            field=models.CharField(blank=True, max_length=127, verbose_name='Yield'),
        ),
        migrations.AlterField(
            model_name='recipepage',
            name='main_image',
            field=models.ForeignKey(help_text='Image should be at least 1280x512 px', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
    ]
