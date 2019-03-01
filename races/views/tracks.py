from django.core.paginator import Paginator
from django.views import generic

from races.models.racetime import RaceTime
from races.models.track import Track


class TrackList(generic.ListView):
    model = Track
    ordering = ['name']
    paginate_by = 10


class TrackDetail(generic.DetailView):
    model = Track

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        filtered_times = RaceTime.objects.filter(track=data['track'])
        fastest_time = filtered_times.order_by('race_duration').first()
        sorted_recent_times = filtered_times.order_by('vehicle_model_id', 'race_duration').distinct('vehicle_model_id')
        latest_time = sorted_recent_times.first()
        track_times = Paginator(sorted_recent_times, 10).get_page(self.request.GET.get('page'))

        data.update({
            'fastest_time': fastest_time,
            'latest_time': latest_time if latest_time != fastest_time else None,
            'track_times': track_times,
            'racetime_columns': ('placement', 'player', 'vehicle', 'duration')
        })

        return data
