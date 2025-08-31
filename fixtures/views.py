from django.views.generic import ListView
from .models import Fixture, Category
from collections import OrderedDict
from django.utils import timezone
from django.db.models import F
from sponsors.models import Sponsor

class FixtureListView(ListView):
    model = Fixture
    template_name = 'fixtures/fixture_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sponsors'] = Sponsor.objects.all()
        
        # Obtenemos TODOS los partidos activos, sin filtro de fecha
        fixtures = Fixture.objects.order_by(
            'category__order',
            'category__name', 
            'display_order', 
            F('match_datetime').asc(nulls_last=True)
        )
        
        # Agrupamos por categoría
        grouped_by_category = OrderedDict()
        for fixture in fixtures:
            category = fixture.category
            if category not in grouped_by_category:
                grouped_by_category[category] = []
            grouped_by_category[category].append(fixture)
            
        context['grouped_by_category'] = grouped_by_category
        return context