from django import forms

from races.models.game import Game
from races.models.player import Player


class PlayerCompareForm(forms.Form):
    game = forms.ModelChoiceField(Game.objects.all(), required=True)
    matching_only = forms.BooleanField(required=False)
    player_fields = []

    def __init__(self, *args, **kwargs):
        self.player_fields = []
        players = Player.objects.all()
        matching_only = kwargs.pop('matching_only', None)
        self.max_compares = kwargs.pop('max_compares')
        min_compares = kwargs.pop('min_compares')
        player_ids = kwargs.pop('player_ids', None)
        player_iterator = iter(player_ids) if player_ids else None
        game_id = kwargs.pop('game_id', None)
        super(PlayerCompareForm, self).__init__(*args, **kwargs)
        self.fields['game'].initial = game_id
        self.fields['matching_only'].initial = matching_only
        for x in range(0, self.max_compares):
            required = x < min_compares
            try:
                player = player_iterator.__next__() if player_iterator else None
            except StopIteration:
                player = None

            player_field = forms.ModelChoiceField(players, required=required, label='Player {:d}'.format(x + 1),
                                                  initial=player)
            player_field_name = 'player{:d}'.format(x + 1)
            self.fields[player_field_name] = player_field
            self.player_fields.append(self[player_field_name])
