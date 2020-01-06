# Generated by Django 2.2.8 on 2020-01-06 18:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0018_auto_20200106_1745'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipepage',
            name='main_image',
            field=models.ForeignKey(help_text='Image should be at least 1920x768 px', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='images.CustomImage'),
        ),
    ]
