from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
