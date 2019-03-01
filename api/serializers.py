from rest_framework import serializers

from races.models.player import Player
from races.models.racetime import RaceTime


class RaceTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceTime
        fields = ('id', 'race_duration', 'player', 'track')


class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Player
        fields = ('id', 'first_name', 'last_name', 'nickname')
