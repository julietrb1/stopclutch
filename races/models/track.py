from random import randint

from django.db import models
from django.db.models import Count


class TrackManager(models.Manager):
    def random(self):
        if not self.count():
            return None

        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Track(models.Model):
    class Meta:
        ordering = ('name',)

    objects = TrackManager()
    name = models.CharField(max_length=50, unique=True)

    def fastest_time(self):
        return self.racetime_set.order_by('race_duration').first()

    def __str__(self):
        return self.name
