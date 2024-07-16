from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('like/<uuid:post_id>/', views.like_post, name='like_post'),
    path('', views.feed, name='feed'),
    path('upload/', views.upload, name='upload'),
    path('profil/', views.profil, name='profil'),
    path('login/', auth_views.LoginView.as_view(template_name='hobbyHub/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='logout_page'), name='logout'),
    path('registrierung/', views.registrierung, name='registrierung'),
    path('profile/edit/', views.profil_bearbeiten, name='profile_edit'),
    path('logout_page/', views.logout_page, name='logout_page'),
    path('feed', views.feed, name='feed'),
    path('profil/<str:benutzername>/', views.benutzer_profil, name='benutzer_profil'), 
    path('profil/<str:benutzername>/follow/', views.follow_user, name='follow_user'),  
    path('add_comment/<str:beitrag_id>/', views.add_comment, name='add_comment'),
]
