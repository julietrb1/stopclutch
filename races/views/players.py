from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic

from races.forms import PlayerCompareForm
from races.models.game import Game
from races.models.player import Player
from races.models.racetime import RaceTime
from races.models.track import Track
from races.models.vehiclemodel import VehicleModel


class PlayerList(generic.ListView):
    model = Player
    ordering = ['first_name', 'last_name']
    paginate_by = 10


class PlayerDetail(generic.DetailView):
    model = Player

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        recent_times = RaceTime.objects.filter(player=data['player']).order_by('-race_date_time')
        data['player_detail_times'] = Paginator(recent_times, 10).get_page(self.request.GET.get('page'))
        data['racetime_columns'] = ('when', 'placement', 'vehicle', 'track', 'duration')
        return data


def compare(request):
    min_compares = 2
    max_compares = 3
    context = {'player_compare_form': PlayerCompareForm(min_compares=min_compares, max_compares=max_compares)}

    try:
        game = Game.objects.get(id=request.GET.get('game'))
    except Game.DoesNotExist:
        return render(request, 'races/player_compare.html', context)

    matching_only = request.GET.get('matching_only')

    player_ids = []
    for x in range(0, max_compares):
        player_id_param = request.GET.get('player{:d}'.format(x + 1))
        if player_id_param:
            player_ids.append(player_id_param)

    player_groups = {}
    if not player_ids:
        return render(request, 'races/player_compare.html', context)

    for player_id in player_ids:
        if player_id.isdigit():
            try:
                player = Player.objects.get(id=int(player_id))
            except Player.DoesNotExist:
                return render(request, 'races/player_compare.html', context)

            player_groups[int(player_id)] = {'player': player, 'wins': 0, 'winner': False}

    player_compare_form = PlayerCompareForm(min_compares=min_compares, max_compares=max_compares, player_ids=player_ids,
                                            game_id=game.id, matching_only=matching_only)
    context['player_compare_form'] = player_compare_form

    racetime_groups = []
    for track in Track.objects.all().order_by('name'):
        for model in VehicleModel.objects.all().order_by('make__name', 'name'):
            temptimes = []
            fastest_time = None

            if matching_only and not verify_matching_only(game, model, player_groups, track):
                continue

            for player in player_groups:
                time_queryset = RaceTime.objects.filter(track=track, vehicle_model=model, player=player, game=game)
                if time_queryset.count():
                    time = time_queryset.first()
                    if not fastest_time or fastest_time.race_duration > time.race_duration:
                        fastest_time = time

                    temptimes.append(time_queryset.first())
                else:
                    temptimes.append(None)

            if fastest_time:
                racetime_groups.append(
                    {'track': track, 'model': model, 'times': temptimes, 'fastest_time': fastest_time})
                player_groups[fastest_time.player.id]['wins'] += 1

    max_wins = 0
    winner = None
    for group_id, group in player_groups.items():
        if group['wins'] == max_wins:
            winner = None

        elif group['wins'] > max_wins:
            winner = group
            max_wins = group['wins']

    if winner:
        player_groups[winner['player'].id]['winner'] = True

    context['racetime_groups'] = racetime_groups
    context['player_groups'] = player_groups

    if not racetime_groups:
        messages.warning(request, 'No race categories were found with your chosen filters.')

    return render(request, 'races/player_compare.html', context)


def verify_matching_only(game, model, player_groups, track):
    category_filter = RaceTime.objects.filter(track=track, vehicle_model=model, game=game)
    for player in player_groups:
        if not category_filter.filter(player=player).count():
            return False

    return True
