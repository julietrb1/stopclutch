from datetime import timedelta

from django.template.loader import get_template
from django.urls import reverse
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.request import Request
from rest_framework.response import Response

import emails
from api import utils
from api.models import VehicleModelCode, TrackCode
from api.serializers import PlayerSerializer, RaceTimeSerializer
from races.models.game import Game
from races.models.player import Player
from races.models.racetime import RaceTime
from races.models.track import Track
from races.models.vehiclemake import VehicleMake
from races.models.vehiclemodel import VehicleModel
from stopclutch import settings


class PlayerList(generics.ListAPIView):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer


class AssettoTimeCreate(generics.CreateAPIView):
    queryset = RaceTime.objects.none()
    serializer_class = RaceTimeSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.DjangoModelPermissions)

    def post(self, request: Request, *args, **kwargs):
        player_id = request.data.get('player_id')
        vehicle_code_name = request.data.get('vehicle_name')
        track_code_name = request.data.get('track_name')
        best_lap_ms = request.data.get('best_lap_ms')
        req_vehicle_make_name = request.data.get('vehicle_make_name')
        req_vehicle_model_name = request.data.get('vehicle_model_name')
        req_track_name = request.data.get('track_name_proper')

        race_duration = timedelta(milliseconds=best_lap_ms)
        player = Player.objects.get(id=player_id)
        assetto, assetto_created = Game.objects.get_or_create(name='Assetto Corsa')

        try:
            vehicle_model_code = VehicleModelCode.objects.get(model_code=vehicle_code_name, game=assetto)
        except VehicleModelCode.DoesNotExist:
            if req_vehicle_make_name and req_vehicle_model_name:
                make_formatted = req_vehicle_make_name
                model_formatted = req_vehicle_model_name
            else:
                make_formatted, model_formatted = utils.extract_vehicle_name(vehicle_code_name)

            if not make_formatted:
                return Response("An empty vehicle make name is not allowed", status=status.HTTP_400_BAD_REQUEST)

            if not model_formatted:
                return Response("An empty vehicle model name is not allowed", status=status.HTTP_400_BAD_REQUEST)

            vehicle_make, vehicle_make_created = VehicleMake.objects.get_or_create(
                name__iexact=make_formatted, defaults={'name': make_formatted})

            vehicle_model, vehicle_model_created = VehicleModel.objects.get_or_create(make=vehicle_make,
                                                                                      name__iexact=model_formatted,
                                                                                      defaults={
                                                                                          'name': model_formatted})

            vehicle_model_code = VehicleModelCode.objects.create(model=vehicle_model, model_code=vehicle_code_name,
                                                                 game=assetto)

        try:
            track_code = TrackCode.objects.get(track_code=track_code_name, game=assetto)
        except TrackCode.DoesNotExist:
            if req_track_name:
                track_name_formatted = req_track_name
            else:
                track_name_formatted = utils.extract_track_name(track_code_name)

            if not track_name_formatted:
                return Response("An empty track name is not allowed", status=status.HTTP_400_BAD_REQUEST)

            track, track_created = Track.objects.get_or_create(name__iexact=track_name_formatted,
                                                               defaults={'name': track_name_formatted})

            track_code = TrackCode.objects.create(track_code=track_code_name, game=assetto, track=track)

        # Manage other category times before saving
        category_times = RaceTime.objects.filter(track=track_code.track, vehicle_model=vehicle_model_code.model,
                                                 game=assetto,
                                                 player=player)

        faster_times = category_times.filter(race_duration__lt=race_duration).order_by('race_duration')
        if faster_times.count():
            response_template = "Race time ignored since {:s} already has a faster race time of {:s} on {:s}" \
                                " with {:s} in {:s}"

            response_msg = response_template \
                .format(player.first_name, str(faster_times[0].race_duration), track_code.track.name,
                        vehicle_model_code.model.__str__(),
                        assetto.name)
            return Response(response_msg, status=status.HTTP_409_CONFLICT)

        equal_times = category_times.filter(race_duration__exact=race_duration)
        if equal_times:
            response_template = "Race time ignored since a race time of {:s} already exists for {:s} on {:s} with" \
                                " {:s} in {:s}"

            response_msg = response_template.format(str(race_duration), player.first_name, track_code.track.name,
                                                    vehicle_model_code.model.__str__(),
                                                    assetto.name)
            return Response(response_msg, status=status.HTTP_409_CONFLICT)

        slower_times = category_times.filter(race_duration__gt=race_duration)
        if slower_times.count():
            response_status = status.HTTP_200_OK
            racetime = slower_times[0]
            racetime.race_duration = race_duration
            racetime.race_date_time = timezone.now()
            racetime.save()
        else:
            response_status = status.HTTP_201_CREATED
            racetime = RaceTime.objects.create(race_duration=race_duration,
                                               race_date_time=timezone.now(),
                                               player=player,
                                               track=track_code.track,
                                               vehicle_model=vehicle_model_code.model,
                                               game=assetto)

        debug_indicator = ' [DEV]' if settings.DEBUG else ''
        email_subject = 'Stopclutch{:s}: New time from {:s}'.format(debug_indicator, racetime.player.__str__())
        email_context = {
            'racetime': racetime,
            'environment': 'DEV' if settings.DEBUG else None,
            'racetime_url': request.build_absolute_uri(reverse('racetimes:detail', args=(racetime.id,))),
        }
        email_html = get_template('emails/new_race_time.html').render(email_context)
        emails.send_html_mail(email_subject, email_html, (settings.ADMIN_EMAIL_RECIPIENT,))

        serializer = RaceTimeSerializer(racetime, context={'request': request})
        return Response(serializer.data, status=response_status)
