# Generated by Django 4.1 on 2022-11-12 03:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_inventory_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthRecord',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('appointment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.appointment')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.patient')),
            ],
        ),
    ]