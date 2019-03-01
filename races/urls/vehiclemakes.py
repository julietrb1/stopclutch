from django.urls import path

from races.views.vehiclemakes import *

app_name = 'vehiclemakes'
urlpatterns = [
    path('', VehicleMakeList.as_view(), name='index'),
    path('<int:pk>/', VehicleMakeDetail.as_view(), name='detail'),
]
