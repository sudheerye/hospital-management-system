# Generated by Django 4.1 on 2022-09-16 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_user_doctor_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctordetails',
            name='doctor',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='app.user'),
        ),
    ]
