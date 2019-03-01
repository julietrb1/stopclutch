from django.urls import path

from races.views.games import *

app_name = 'games'
urlpatterns = [
    path('', GameList.as_view(), name='index'),
    path('<int:pk>/', GameDetail.as_view(), name='detail'),
]
