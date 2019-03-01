from django.urls import path

from races.views import players as views

app_name = 'players'
urlpatterns = [
    path('', views.PlayerList.as_view(), name='index'),
    path('<int:pk>/', views.PlayerDetail.as_view(), name='detail'),
    path('compare/', views.compare, name='compare')
]
