from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('music/', views.music_platform, name='music_platform'),
]
