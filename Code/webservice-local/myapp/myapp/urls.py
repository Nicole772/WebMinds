"""
URL configuration for myapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import TemplateView
from django.conf.urls.static import static

from . import myController

urlpatterns = [
    path("", myController.index2, name="index"),
	path("paramsToJson", myController.paramsToJson, name="paramsToJson"),
	path("Hello", myController.Hello, name="Hello"),
	path("Nominativi", myController.Nominativi, name="Nominativi"),
	path("StartSession", myController.StartSession, name="StartSession"),
	path("CloseSession", myController.CloseSession, name="CloseSession"),
	path("SessionCount", myController.SessionCount, name="SessionCount")]
    path('importa-dati/', myController.ImportaDatiAltervista, name='importa-dati'),
    path('test-connessione/', myController.TestConnessione, name='test-connessione'),

