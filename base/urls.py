from django.urls import path
from . import views #import views.py from the current directory

urlpatterns = [
    path('', views.home, name = "home"),
    path('room/', views.room, name = "room"),
    #path('nav/', views.nav, name="navbar")
]
