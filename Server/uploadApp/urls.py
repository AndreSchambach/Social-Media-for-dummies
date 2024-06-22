from django.urls import path
from uploadApp import views

urlpatterns = [
    path("test/home", views.home, name ="home"),
    path("socialmedia/upload", views.upload, name = "upload"),
]