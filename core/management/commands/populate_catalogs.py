from django.core.management.base import BaseCommand
from members.models import MemberType, Category, SpecificPosition
from news.models import NewsCategory
from fixtures.models import Team # Importamos Team para crear a Olimpo

class Command(BaseCommand):
    help = 'Creates all the necessary catalog data.'

    def handle(self, *args, **kwargs):
        self.stdout.write('--- Creando catálogos base ---')
        
        # ELIMINAMOS EL BORRADO DESDE AQUÍ.
        # El borrado principal se hará en el script populate_all.
        
        MemberType.objects.get_or_create(name='Socio Jugador')
        MemberType.objects.get_or_create(name='Staff')
        MemberType.objects.get_or_create(name='Socio Dirigente')

        cargos = ['Arquero', 'Defensor', 'Mediocampista', 'Delantero', 'Director Técnico', 'Ayudante de Campo', 'Preparador Físico', 'Presidente', 'Vicepresidente', 'Secretario', 'Tesorero', 'Vocal Titular', 'Vocal Suplente', 'Fiscalizador']
        for cargo in cargos:
            SpecificPosition.objects.get_or_create(name=cargo)

        categorias_info = [("Primera", 10), ("Sub-17", 20), ("Sub-15", 30), ("Sub-13", 40), ("Sub-11", 50), ("Sub-9", 60), ("Sub-7", 70)]
        for nombre, orden in categorias_info:
            Category.objects.get_or_create(name=nombre, defaults={'order': orden})

        for name in ['Resultados', 'Eventos del Club', 'Institucional', 'Entrevistas']:
            NewsCategory.objects.get_or_create(name=name, defaults={'slug': name.lower()})

        # Nos aseguramos de que el equipo 'Olimpo' exista para el script de fixtures
        Team.objects.get_or_create(name="Olimpo")

        self.stdout.write(self.style.SUCCESS('Catálogos creados o verificados.'))