from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api import views

urlpatterns = [
    path('players/', views.PlayerList.as_view()),
    path('assetto_times/', views.AssettoTimeCreate.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
