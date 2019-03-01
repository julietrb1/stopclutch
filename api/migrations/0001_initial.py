# Generated by Django 2.0.2 on 2018-02-25 01:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('races', '0008_auto_20180224_2255'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrackCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('track_code', models.CharField(max_length=50)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.Game')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.Track')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleModelCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_code', models.CharField(max_length=50)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.Game')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.VehicleModel')),
            ],
        ),
    ]
