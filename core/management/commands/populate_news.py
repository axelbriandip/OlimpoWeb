from django.core.management.base import BaseCommand
from faker import Faker
from news.models import Article, NewsCategory
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'Creates 40 news articles.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- Creando 40 noticias ---'))
        fake = Faker('es_AR')

        # Asumimos que el superusuario existe y será el autor
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            self.stdout.write(self.style.ERROR('No se encontró un superusuario para asignar como autor.'))
            return

        categorias = [NewsCategory.objects.get_or_create(name=name, slug=name.lower())[0] for name in ['Resultados', 'Eventos del Club', 'Institucional', 'Entrevistas']]

        for _ in range(40):
            title = fake.sentence(nb_words=6)
            Article.objects.create(
                title=title,
                subtitle=fake.sentence(nb_words=12),
                category=random.choice(categorias),
                excerpt=fake.paragraph(nb_sentences=2),
                content=fake.paragraph(nb_sentences=10),
                status='PB', # Publicado
            )
        self.stdout.write(self.style.SUCCESS('40 noticias creadas con éxito.'))