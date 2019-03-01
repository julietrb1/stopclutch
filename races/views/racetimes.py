from django.core.paginator import Paginator
from django.views import generic

from races.models.racetime import RaceTime


class RaceTimeList(generic.ListView):
    model = RaceTime
    ordering = ['-race_date_time']
    paginate_by = 10


class RaceTimeDetail(generic.DetailView):
    model = RaceTime

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        per_page = 10
        data['placement'] = data['racetime'].get_placement()
        default_page = int(data['placement'] / per_page) + 1
        category_times = data['racetime'].get_category_times()
        data['fastest_time'] = category_times[0]
        data['category_times'] = Paginator(category_times, per_page).get_page(
            self.request.GET.get('page', default_page))
        data['racetime_columns'] = ('placement', 'player', 'duration')
        data['mobile_player_only'] = 'player' in data['racetime_columns']
        data['highlighted_placements'] = (data['placement'],)
        return data
