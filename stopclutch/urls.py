"""stopclutch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from races.views import home as home_views
from stopclutch import settings

urlpatterns = [
    path('api/', include('api.urls')),
    path('', home_views.home, name='home'),
    path('faqs', home_views.faqs, name='faqs'),
    path('players/', include('races.urls.players')),
    path('tracks/', include('races.urls.tracks')),
    path('vehiclemakes/', include('races.urls.vehiclemakes')),
    path('vehiclemodels/', include('races.urls.vehiclemodels')),
    path('racetimes/', include('races.urls.racetimes')),
    path('games/', include('races.urls.games')),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
