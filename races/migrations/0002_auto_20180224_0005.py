# Generated by Django 2.0.2 on 2018-02-23 11:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('races', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='racetime',
            name='comments',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
