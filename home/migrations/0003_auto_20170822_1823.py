# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneralSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(help_text='Website name', max_length=127)),
                ('site_tagline', models.CharField(blank=True, help_text='Tagline to show after the site title', max_length=255)),
                ('site_description', models.TextField(blank=True, help_text='Description of website (to appear on searches)')),
                ('pagination_count', models.PositiveIntegerField(default=10, help_text='Number of posts to display per page on index pages')),
                ('disqus', models.CharField(blank=True, help_text='Site name on Disqus. Comments will only appear if this is provided.', max_length=127, null=True)),
                ('google_analytics_id', models.CharField(blank=True, help_text='Google Analytics Tracking ID', max_length=127, null=True)),
                ('google_custom_search_key', models.CharField(blank=True, help_text='Unique ID for Google Custom Search', max_length=127, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='homepage',
            options={'verbose_name': 'Homepage'},
        ),
        migrations.AddField(
            model_name='homepage',
            name='body',
            field=wagtail.wagtailcore.fields.RichTextField(blank=True),
        ),
    ]