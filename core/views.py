from django.shortcuts import render
from news.models import Article
from fixtures.models import Fixture
from .models import BoardMember
from django.utils import timezone
from collections import OrderedDict

def home(request):
    # Vista para la página de inicio.
    latest_articles = Article.objects.filter(status='PB').order_by('-created_on')[:3]
    next_fixture = Fixture.objects.filter(match_datetime__gte=timezone.now()).order_by('match_datetime').first()
    
    context = {
        'latest_articles': latest_articles,
        'next_fixture': next_fixture,
    }
    return render(request, 'core/home.html', context)

def history(request):
    # Vista para la página de 'Nuestra Historia'.
    return render(request, 'core/history.html')

def board_of_directors(request):
    members = BoardMember.objects.all()
    
    # Creamos un diccionario para agrupar los miembros
    grouped_members = OrderedDict()
    
    # Definimos el orden en que queremos que aparezcan los grupos
    group_order = ['Mesa Directiva', 'Vocales', 'Comisión Fiscalizadora']

    for group in group_order:
        # Filtramos los miembros para cada grupo
        members_in_group = [m for m in members if m.group == group]
        if members_in_group:
            grouped_members[group] = members_in_group
            
    context = {
        'grouped_members': grouped_members,
    }
    return render(request, 'core/board_of_directors.html', context)