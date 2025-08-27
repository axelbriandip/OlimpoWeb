from django.urls import path
from .views import PlayerListView, PlayerDetailView

urlpatterns = [
    # URL para la lista de jugadores. ej: misitio.com/players/
    path('', PlayerListView.as_view(), name='player_list'),

    # URL para el detalle de un jugador. ej: misitio.com/players/1/
    path('<int:pk>/', PlayerDetailView.as_view(), name='player_detail'),
]