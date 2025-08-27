from django.views.generic import ListView, DetailView
from .models import Player

# Create your views here.

class PlayerListView(ListView):
    """
    Vista para mostrar la lista de todos los jugadores activos.
    """
    model = Player
    template_name = 'players/player_list.html'
    context_object_name = 'players'

    def get_queryset(self):
        # Nos aseguramos de mostrar solo los jugadores marcados como activos.
        return Player.objects.filter(is_active=True).order_by('last_name')

class PlayerDetailView(DetailView):
    """
    Vista para mostrar los detalles de un único jugador.
    """
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'