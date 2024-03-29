# Generated by Django 2.0.2 on 2018-02-23 10:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('nickname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RaceTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('race_duration', models.DurationField()),
                ('race_date_time', models.DateTimeField(verbose_name='Race date')),
                ('comments', models.TextField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='races.Game')),
                ('player',
                 models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='races.Player')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('variant', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='VehicleMake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('make', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='races.VehicleMake')),
            ],
        ),
        migrations.AddField(
            model_name='racetime',
            name='track',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='races.Track'),
        ),
        migrations.AddField(
            model_name='racetime',
            name='vehicle_model',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='races.VehicleModel'),
        ),
        migrations.AlterUniqueTogether(
            name='vehiclemodel',
            unique_together={('make', 'name')},
        ),
    ]
