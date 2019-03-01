from django.db import models
from django.db.models import CASCADE

from races.models.game import Game
from races.models.track import Track
from races.models.vehiclemodel import VehicleModel


class VehicleModelCode(models.Model):
    model_code = models.CharField(max_length=50)
    game = models.ForeignKey(Game, on_delete=CASCADE)
    model = models.OneToOneField(VehicleModel, on_delete=CASCADE)

    def __str__(self):
        return "{:s} {:s} / {:s}".format(self.model.make.name, self.model.name, self.model_code)


class TrackCode(models.Model):
    track_code = models.CharField(max_length=50, unique=True)
    game = models.ForeignKey(Game, on_delete=CASCADE)
    track = models.OneToOneField(Track, on_delete=CASCADE)

    def __str__(self):
        return "{:s} / {:s}".format(self.track.name, self.track_code)
