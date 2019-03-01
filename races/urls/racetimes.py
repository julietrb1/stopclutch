from django.urls import path

from races.views.racetimes import *

app_name = 'racetimes'
urlpatterns = [
    path('', RaceTimeList.as_view(), name='index'),
    path('<int:pk>/', RaceTimeDetail.as_view(), name='detail'),
]
