from django.core.paginator import Paginator
from django.views import generic

from races.models.racetime import RaceTime
from races.models.vehiclemodel import VehicleModel


class VehicleModelList(generic.ListView):
    model = VehicleModel
    ordering = ['make__name', 'name']
    paginate_by = 10


class VehicleModelDetail(generic.DetailView):
    model = VehicleModel

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        filtered_times = RaceTime.objects.filter(vehicle_model=data['vehiclemodel'])
        data['fastest_time'] = filtered_times.order_by('race_duration').first()
        sorted_recent_times = filtered_times.order_by('track_id', 'race_duration').distinct('track_id')
        data['most_recent_time'] = sorted_recent_times.first()
        data['recent_times'] = Paginator(sorted_recent_times, 10).get_page(self.request.GET.get('page'))
        data['racetime_columns'] = ('placement', 'player', 'track', 'duration')
        return data
