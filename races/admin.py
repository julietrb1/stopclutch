from django import forms
from django.contrib import admin

from races.models.game import Game
from races.models.player import Player
from races.models.racetime import RaceTime
from races.models.track import Track
from races.models.vehiclemake import VehicleMake
from races.models.vehiclemodel import VehicleModel


class RaceTimeForm(forms.ModelForm):
    class Meta:
        model = RaceTime
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        track = cleaned_data.get('track')
        model = cleaned_data.get('vehicle_model')
        game = cleaned_data.get('game')
        player = cleaned_data.get('player')
        race_duration = cleaned_data.get('race_duration')

        category_times = RaceTime.objects.filter(track=track, vehicle_model=model,
                                                 game=game,
                                                 player=player)

        if self.instance.pk:
            category_times = category_times.exclude(id=self.instance.pk)

        slower_times = category_times.filter(race_duration__gt=race_duration)

        if slower_times.count():
            slower_times.delete()

        faster_times = category_times.filter(race_duration__lt=race_duration).order_by('race_duration')
        if faster_times.count():
            raise forms.ValidationError(
                "A faster time of {:s} already exists".format(str(faster_times[0].race_duration)))

        equal_times = category_times.filter(race_duration__exact=race_duration)
        if equal_times:
            raise forms.ValidationError(
                "An equal time of {:s} already exists".format(str(equal_times[0].race_duration)))

        return cleaned_data


class GameAdmin(admin.ModelAdmin):
    ordering = ['name']


class PlayerAdmin(admin.ModelAdmin):
    ordering = ('first_name', 'last_name', 'nickname')


class RaceTimeAdmin(admin.ModelAdmin):
    form = RaceTimeForm
    list_display = ('race_date_time', 'race_duration', 'player', 'track', 'vehicle_model', 'game')


class TrackAdmin(admin.ModelAdmin):
    ordering = ('name',)


admin.site.register(Game, GameAdmin)
admin.site.register(Player, PlayerAdmin)
admin.site.register(RaceTime, RaceTimeAdmin)
admin.site.register(Track, TrackAdmin)
admin.site.register(VehicleMake)
admin.site.register(VehicleModel)
