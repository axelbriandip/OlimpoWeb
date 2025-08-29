from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('history/', views.history, name='history'),
    path('board-of-directors/', views.board_of_directors, name='board_of_directors'),
]