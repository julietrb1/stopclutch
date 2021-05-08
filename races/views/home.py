from django.shortcuts import render

from races.models.game import Game
from races.models.player import Player
from races.models.racetime import RaceTime
from races.models.track import Track
from races.models.vehiclemodel import VehicleModel


def home(request):
    player_count = Player.objects.count()
    random_player = Player.objects.random()
    random_track = Track.objects.random()
    random_vehicle = VehicleModel.objects.random()
    context = {'race_time_count': RaceTime.objects.count(),
               'player_count': player_count,
               'track_count': Track.objects.count(),
               'vehicle_count': VehicleModel.objects.count(),
               'most_recent_race_time': RaceTime.objects.order_by('-race_date_time').first(),
               'first_game': Game.objects.order_by('name').first(),
               'random_player': random_player,
               'random_track': random_track,
               'random_vehicle': random_vehicle}
    return render(request, 'races/home.html', context)


def faqs(request):
    context = {'first_game': Game.objects.order_by('name').first()}
    return render(request, 'races/faqs.html', context)
