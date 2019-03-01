# Generated by Django 2.0.2 on 2018-03-02 04:06

from django.db import migrations


def combine_track_name_and_variant(apps, schema_editor):
    Track = apps.get_model('races', 'Track')
    for track in Track.objects.all():
        if track.variant:
            track.name += ' - {:s}'.format(track.variant)
            track.save()


class Migration(migrations.Migration):
    dependencies = [
        ('races', '0010_auto_20180226_1910'),
    ]

    operations = [
        migrations.RunPython(
            combine_track_name_and_variant
        ),

    ]
