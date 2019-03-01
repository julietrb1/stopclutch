from random import randint

from django.db import models
from django.db.models import CASCADE, Count

from races.models.vehiclemake import VehicleMake


class VehicleModelManager(models.Manager):
    def random(self):
        if not self.count():
            return None

        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class VehicleModel(models.Model):
    class Meta:
        unique_together = ('make', 'name')
        ordering = ('make__name', 'name')

    objects = VehicleModelManager()
    make = models.ForeignKey(VehicleMake, on_delete=CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return "{:s} {:s}".format(self.make.name, self.name)
