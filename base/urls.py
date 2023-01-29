from django.urls import path
from . import views #import views.py from the current directory

urlpatterns = [
    path('', views.home, name = "home"),
    path('room/<str:pk>/', views.room, name = "room"),
    #path('nav/', views.nav, name="navbar")
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerUser,name="register"),
    path('delete-message/<str:pk>',views.deleteMessage,name='delete'),
    path('user/<str:pk>/', views.userProfile, name = "user"),

    path('create-room/',views.createRoom,name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom,name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom,name="delete-room")

]
