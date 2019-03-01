from django.core.paginator import Paginator
from django.db.models import Count
from django.views import generic

from races.models.game import Game
from races.models.player import Player
from races.models.racetime import RaceTime


class GameList(generic.ListView):
    model = Game
    ordering = ['name']
    paginate_by = 10


class GameDetail(generic.DetailView):
    model = Game

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        sorted_race_times = RaceTime.objects.filter(game=data['game']).order_by('-race_date_time')
        data['recent_game_times'] = Paginator(sorted_race_times, 10).get_page(self.request.GET.get('page'))
        data['frequent_players'] = Player.objects.filter(racetime__game=data['game']).annotate(
            race_time_count=Count('racetime')).order_by('-race_time_count', 'first_name')[:5]
        data['racetime_columns'] = ('placement', 'player', 'vehicle', 'track', 'duration')
        return data
