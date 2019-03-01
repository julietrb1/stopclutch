from django.db import models
from django.utils import timezone

from races.models.game import Game
from races.models.player import Player
from races.models.track import Track
from races.models.vehiclemodel import VehicleModel


class RaceTime(models.Model):
    class Meta:
        ordering = ['-race_date_time', 'player']

    race_duration = models.DurationField()
    race_date_time = models.DateTimeField(verbose_name='Race date', default=timezone.now)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE)
    comments = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_placement(self):
        return RaceTime.objects.filter(track=self.track, vehicle_model=self.vehicle_model,
                                       game=self.game, race_duration__lt=self.race_duration) \
                   .order_by('race_duration').count() + 1

    def get_category_times(self):
        return RaceTime.objects.filter(track=self.track, vehicle_model=self.vehicle_model,
                                       game=self.game).order_by('race_duration')

    def __str__(self):
        return "{:s} @ {:s} / {:s}".format(self.player.__str__(), self.track.name, self.vehicle_model.name)
