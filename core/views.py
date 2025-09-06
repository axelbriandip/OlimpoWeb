from django.shortcuts import render
from news.models import Article
from sponsors.models import Sponsor
from fixtures.models import Fixture
from .models import BoardMember, TimelineEvent, Testimonial
from gallery.models import  Album
from django.utils import timezone
from collections import OrderedDict
from members.models import Profile, Role

def home(request):
    # Vista para la página de inicio.
    latest_articles = Article.objects.filter(status='PB').order_by('-created_on')[:3]
    next_fixture = Fixture.objects.filter(match_datetime__gte=timezone.now()).order_by('match_datetime').first()
    sponsors = Sponsor.objects.all()
    featured_testimonials = Testimonial.objects.filter(is_featured=True)
    latest_albums = Album.objects.order_by('-created_on')[:3]
    context = {
        'latest_articles': latest_articles,
        'next_fixture': next_fixture,
        'sponsors': sponsors,
        'featured_testimonials': featured_testimonials,
        'latest_albums': latest_albums,
    }
    return render(request, 'core/home.html', context)

def history(request):
    # Vista para la página de 'Nuestra Historia'.
    return render(request, 'core/history.html')

def board_of_directors(request):
    """
    Muestra a los miembros de la Comisión Directiva, buscando perfiles
    que tengan un rol de tipo 'Dirigente'.
    """
    # Buscamos todos los roles que sean de la función 'Dirigente'
    board_roles = Role.objects.filter(function='DIR').order_by('profile__member_id')
    
    # (Opcional) Si quisieras agruparlos por cargo (Presidente, Tesorero, etc.)
    # podrías añadir una lógica de agrupación aquí, pero por ahora los mostramos todos juntos.

    context = {
        'board_roles': board_roles,
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