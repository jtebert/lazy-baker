# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-22 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.embeds.blocks
import wagtail.images.blocks


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wagtailcore', '0039_collectionviewrestriction'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', wagtail.core.fields.RichTextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RecipeIndexPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('intro', models.TextField(blank=True, help_text='This text will be formatted with markdown.')),
            ],
            options={
                'verbose_name': 'Subject Section',
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='RecipePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('date', models.DateField(verbose_name='Post date')),
                ('intro', models.TextField(help_text='This text will be formatted with markdown.', max_length=250)),
                ('body', wagtail.core.fields.StreamField([('text', wagtail.core.blocks.TextBlock(help_text='This text will be formatted with markdown.', icon='pilcrow')), ('image', wagtail.core.blocks.StructBlock([(b'image', wagtail.images.blocks.ImageChooserBlock()), (b'caption', wagtail.core.blocks.CharBlock(blank=True, help_text='This will override the default caption.This text will be formatted with markdown.', null=True, required=False))])), ('embed', wagtail.embeds.blocks.EmbedBlock(icon='media')), ('pull_quote', wagtail.core.blocks.StructBlock([(b'quote', wagtail.core.blocks.TextBlock()), (b'author', wagtail.core.blocks.CharBlock())]))])),
                ('main_image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage')),
            ],
            options={
                'verbose_name': 'Recipe',
            },
            bases=('wagtailcore.page',),
        ),
    ]
