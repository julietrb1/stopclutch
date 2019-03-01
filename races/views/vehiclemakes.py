from django.views import generic

from races.models.racetime import RaceTime
from races.models.vehiclemake import VehicleMake
from races.models.vehiclemodel import VehicleModel


class VehicleMakeList(generic.ListView):
    model = VehicleMake
    ordering = ['name']
    paginate_by = 10


class VehicleMakeDetail(generic.DetailView):
    model = VehicleMake

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        make = data['vehiclemake']
        data['model_list'] = VehicleModel.objects.filter(make=make).order_by('name')
        data['recent_times'] = RaceTime.objects.filter(vehicle_model__make=make).order_by('vehicle_model_id',
                                                                                          'track_id',
                                                                                          'race_duration').distinct(
            'vehicle_model_id', 'track_id')[:10]
        data['racetime_columns'] = ('placement', 'player', 'vehicle', 'track', 'duration')
        return data
