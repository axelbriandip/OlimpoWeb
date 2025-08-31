from django.shortcuts import render
from news.models import Article
from sponsors.models import Sponsor
from fixtures.models import Fixture
from .models import BoardMember, TimelineEvent, Testimonial
from django.utils import timezone
from collections import OrderedDict

def home(request):
    # Vista para la página de inicio.
    latest_articles = Article.objects.filter(status='PB').order_by('-created_on')[:3]
    next_fixture = Fixture.objects.filter(match_datetime__gte=timezone.now()).order_by('match_datetime').first()
    sponsors = Sponsor.objects.all()
    featured_testimonials = Testimonial.objects.filter(is_featured=True)
    context = {
        'latest_articles': latest_articles,
        'next_fixture': next_fixture,
        'sponsors': sponsors,
        'featured_testimonials': featured_testimonials,
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
    sponsors = Sponsor.objects.all()

    for group in group_order:
        # Filtramos los miembros para cada grupo
        members_in_group = [m for m in members if m.group == group]
        if members_in_group:
            grouped_members[group] = members_in_group
            
    context = {
        'grouped_members': grouped_members,
        'sponsors': sponsors,
    }
    return render(request, 'core/board_of_directors.html', context)

def history(request):
    """
    Vista para la página de 'Nuestra Historia'.
    """
    # Obtenemos solo los Hitos Principales (los que no tienen padre)
    # y usamos prefetch_related para cargar eficientemente todos sus sub-hitos en una sola consulta.
    main_events = TimelineEvent.objects.filter(parent__isnull=True).prefetch_related('sub_events')
    sponsors = Sponsor.objects.all()
    
    context = {
        'main_events': main_events,
        'sponsors': sponsors,
    }
    return render(request, 'core/history.html', context)