from django.urls import path

from races.views.tracks import *

app_name = 'tracks'
urlpatterns = [
    path('', TrackList.as_view(), name='index'),
    path('<int:pk>/', TrackDetail.as_view(), name='detail'),
]
