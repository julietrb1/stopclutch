from django.urls import path

from races.views.vehiclemodels import *

app_name = 'vehiclemodels'
urlpatterns = [
    path('', VehicleModelList.as_view(), name='index'),
    path('<int:pk>/', VehicleModelDetail.as_view(), name='detail'),
]
