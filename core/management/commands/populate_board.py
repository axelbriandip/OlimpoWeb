from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from members.models import Profile, MemberType, Role, SpecificPosition

class Command(BaseCommand):
    help = 'Creates 8 board members.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- Creando 8 miembros de la Comisión Directiva ---'))
        fake = Faker('es_AR')

        socio_dirigente = MemberType.objects.get(name='Socio Dirigente')
        cargos = ['Presidente', 'Vicepresidente', 'Secretario', 'Tesorero', 'Vocal Titular', 'Vocal Titular', 'Vocal Suplente', 'Fiscalizador']

        for i, cargo in enumerate(cargos):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'dirigente.{i}'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': 'password123',
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if not created: continue

            user.profile.member_type = socio_dirigente
            user.profile.save()

            Role.objects.create(
                profile=user.profile,
                function='DIR',
                category=None, # Los dirigentes no tienen categoría deportiva
                specific_position=SpecificPosition.objects.get(name=cargo)
            )
        self.stdout.write(self.style.SUCCESS('8 miembros de la Comisión Directiva creados con éxito.'))