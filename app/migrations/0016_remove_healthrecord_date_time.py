# Generated by Django 4.1 on 2022-11-12 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_healthrecord'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='healthrecord',
            name='date_time',
        ),
    ]