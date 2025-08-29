from django.shortcuts import render
from news.models import Article
from fixtures.models import Fixture
from .models import BoardMember
from django.utils import timezone

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
    # Vista para la página de la 'Comisión Directiva'.
    members = BoardMember.objects.all()
    context = {
        'members': members,
    }
    return render(request, 'core/board_of_directors.html', context)