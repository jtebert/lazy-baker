# Generated by Django 2.2.8 on 2020-01-06 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_aboutpage'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalsettings',
            name='contact_email',
            field=models.EmailField(blank=True, help_text='Publically displayed contact information', max_length=254),
        ),
    ]
