# Generated by Django 2.0.2 on 2018-02-25 01:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trackcode',
            name='track',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='races.Track'),
        ),
        migrations.AlterField(
            model_name='trackcode',
            name='track_code',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='vehiclemodelcode',
            name='model',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='races.VehicleModel'),
        ),
    ]
