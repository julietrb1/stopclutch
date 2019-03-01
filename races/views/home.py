from django.contrib import messages
from django.shortcuts import render
from django_countries import countries

import emails
from races.forms import InterestForm
from races.models.game import Game
from races.models.player import Player
from races.models.racetime import RaceTime
from races.models.track import Track
from races.models.vehiclemodel import VehicleModel
from stopclutch import settings


def home(request):
    player_count = Player.objects.count()
    random_player = Player.objects.random()
    random_track = Track.objects.random()
    random_vehicle = VehicleModel.objects.random()
    context = {'race_time_count': RaceTime.objects.count(),
               'player_count': player_count,
               'track_count': Track.objects.count(),
               'vehicle_count': VehicleModel.objects.count(),
               'most_recent_race_time': RaceTime.objects.order_by('-race_date_time').first(),
               'first_game': Game.objects.order_by('name').first(),
               'random_player': random_player,
               'random_track': random_track,
               'random_vehicle': random_vehicle}
    return render(request, 'races/home.html', context)


def faqs(request):
    context = {'first_game': Game.objects.order_by('name').first(), 'interest_form': InterestForm()}

    if request.method == 'POST':
        form = InterestForm(request.POST)
        if form.is_valid():
            context['interest_form'] = None
            email_subject = 'Stopclutch expression of interest'
            email_message = '"{:s}" from {:s} ({:s}) has sent you an expression of interest in using Stopclutch publicly.'.format(
                form.cleaned_data['name'], dict(countries)[form.cleaned_data['country']], form.cleaned_data['email'])
            if form.cleaned_data['comments']:
                email_message += '\n\nComments: {:s}'.format(form.cleaned_data['comments'])
            if settings.DEBUG:
                print('Sending email with subject "{:s}" and body:\n{:s}'.format(email_subject, email_message))
            else:
                emails.send_html_mail(email_subject, email_message,
                                      (settings.ADMIN_EMAIL_RECIPIENT,))
            messages.info(request,
                          'Thanks! Your expression of interest has been sent, and I\'ll be more than happy to hear from you.')
        else:
            messages.error(request, form.errors)

    return render(request, 'races/faqs.html', context)
