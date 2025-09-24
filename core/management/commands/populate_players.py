import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from members.models import Profile, MemberType, Role, Category, SpecificPosition

class Command(BaseCommand):
    help = 'Creates 120 player profiles.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- Creando 120 jugadores ---'))
        fake = Faker('es_AR')

        # Asumimos que los catálogos ya fueron creados por un script base
        socio_jugador = MemberType.objects.get(name='Socio Jugador')
        categorias_db = {cat.name: cat for cat in Category.objects.all()}
        posiciones_db = {pos.name: pos for pos in SpecificPosition.objects.all()}

        # Mapeo de categorías a rangos de edad
        cat_ages = {
            "Primera": (18, 35), "Sub-17": (16, 17), "Sub-15": (14, 15),
            "Sub-13": (12, 13), "Sub-11": (10, 11), "Sub-9": (8, 9), "Sub-7": (6, 7)
        }

        for i in range(120):
            cat_nombre, cat_obj = random.choice(list(categorias_db.items()))
            min_age, max_age = cat_ages.get(cat_nombre, (18, 30))

            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'jugador.{i}'

            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': 'password123',
                    'first_name': first_name,
                    'last_name': last_name,
                    'email': fake.email()
                }
            )
            if not created: continue

            user.profile.dni = fake.ssn()
            user.profile.date_of_birth = fake.date_of_birth(minimum_age=min_age, maximum_age=max_age)
            user.profile.member_type = socio_jugador
            user.profile.is_on_roster = True
            user.profile.save()

            Role.objects.create(
                profile=user.profile,
                function='JUG',
                category=cat_obj,
                specific_position=posiciones_db[random.choice(['Arquero', 'Defensor', 'Mediocampista', 'Delantero'])]
            )

        self.stdout.write(self.style.SUCCESS('120 jugadores creados con éxito.'))