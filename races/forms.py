from captcha.fields import ReCaptchaField
from django import forms
from django.forms.utils import ErrorList
from django_countries import countries
from django_countries.widgets import CountrySelectWidget

from races.models.game import Game
from races.models.player import Player
from stopclutch import settings


class InterestForm(forms.Form):
    name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=100, required=True)
    country = forms.ChoiceField(choices=countries, widget=CountrySelectWidget)
    comments = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 2}), required=False)

    def __init__(self, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, field_order=None, use_required_attribute=None,
                 renderer=None):
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, field_order,
                         use_required_attribute, renderer)

        if not settings.DEBUG:
            self.fields['captcha'] = ReCaptchaField()


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
