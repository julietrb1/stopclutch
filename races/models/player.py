from random import randint

from django.db import models
from django.db.models import Count


class PlayerManager(models.Manager):
    def random(self):
        if not self.count():
            return None

        count = self.aggregate(count=Count('id'))['count']
        random_index = randint(0, count - 1)
        return self.all()[random_index]


class Player(models.Model):
    class Meta:
        unique_together = ('first_name', 'last_name')
        ordering = ('first_name', 'last_name', 'nickname')

    objects = PlayerManager()
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=50, unique=True, null=True, blank=True)

    def __str__(self):
        if self.nickname:
            return "{:s} \"{:s}\" {:s}.".format(self.first_name, self.nickname, self.last_name[:1])
        elif self.last_name:
            return "{:s} {:s}.".format(self.first_name, self.last_name[:1])
        else:
            return self.first_name
