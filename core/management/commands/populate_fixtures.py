import random
from django.core.management.base import BaseCommand
from faker import Faker
from fixtures.models import Team, Fixture
from members.models import Category
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates 40 fixtures.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- Creando 40 partidos ---'))
        fake = Faker('es_AR')

        # Creamos equipos rivales si no existen
        rivales = []
        for _ in range(20):
            team_name = fake.company() + " FC"
            rival, created = Team.objects.get_or_create(name=team_name)
            rivales.append(rival)
        
        olimpo = Team.objects.get(name__iexact="Olimpo")
        categorias = list(Category.objects.all())
        torneos = ["Clausura 'A'", "Copa Ciudad", "Torneo Provincial"]
        etapas = [f"Fecha {i}" for i in range(1, 15)]

        for i in range(40):
            Fixture.objects.create(
                home_team=olimpo,
                away_team=random.choice(rivales),
                home_score=random.randint(0, 4) if i % 2 == 0 else None,
                away_score=random.randint(0, 3) if i % 2 == 0 else None,
                match_datetime=timezone.now() + timedelta(days=random.randint(-15, 30)),
                venue=fake.city(),
                league_name="Liga Independiente",
                tournament_name=random.choice(torneos),
                stage=random.choice(etapas),
                category=random.choice(categorias),
                display_order=i * 10
            )

        self.stdout.write(self.style.SUCCESS('40 partidos creados con éxito.'))