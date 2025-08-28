from collections import OrderedDict
from django.views.generic import ListView, DetailView
from .models import Player, Category
from django.db.models import Q

class PlayerListView(ListView):
    model = Player
    template_name = 'players/player_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # --- 1. Lógica de Filtro ---
        all_players = Player.objects.filter(is_active=True).order_by('last_name')
        context['categories'] = Category.objects.all() # Las categorías para los botones ahora vienen de la DB
        
        selected_category_name = self.request.GET.get('category')
        players_to_display = all_players
        
        if selected_category_name:
            # Filtramos jugadores cuya categoría de edad calculada coincida
            filtered_players = [p for p in all_players if p.age_category == selected_category_name]
            
            # Filtramos cuerpo técnico que tenga asignada esa categoría
            filtered_staff = all_players.filter(
                managed_categories__name=selected_category_name
            )
            
            # Combinamos ambos resultados y eliminamos duplicados
            players_to_display = list(set(filtered_players) | set(filtered_staff))
            context['selected_category'] = selected_category_name

        # --- 2. Lógica de Agrupación (sin cambios) ---
        grouped_players = OrderedDict()
        position_map = OrderedDict([
            ('Arqueros', ['Arquero']),
            ('Defensores', ['Defensor']),
            ('Mediocampistas', ['Mediocampista']),
            ('Delanteros', ['Delantero']),
            ('Cuerpo Técnico', ['Director Técnico', 'Ayudante de Campo', 'Preparador Físico'])
        ])

        for group_title, positions_in_group in position_map.items():
            players_in_group = sorted(
                [p for p in players_to_display if p.position in positions_in_group],
                key=lambda x: x.last_name # Aseguramos el orden
            )
            if players_in_group:
                grouped_players[group_title] = players_in_group
        
        context['grouped_players'] = grouped_players
        return context


# La PlayerDetailView no cambia
class PlayerDetailView(DetailView):
    model = Player
    template_name = 'players/player_detail.html'
    context_object_name = 'player'