import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from members.models import Profile, MemberType, Role, Category, SpecificPosition

class Command(BaseCommand):
    help = 'Creates 25 staff members.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- Creando 25 miembros del Cuerpo Técnico ---'))
        fake = Faker('es_AR')

        socio_staff = MemberType.objects.get(name='Staff')
        categorias = list(Category.objects.all())
        posiciones_staff = [SpecificPosition.objects.get(name=name) for name in ['Director Técnico', 'Ayudante de Campo', 'Preparador Físico']]

        for i in range(25):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f'staff.{i}'
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'password': 'password123',
                    'first_name': first_name,
                    'last_name': last_name
                }
            )
            if not created: continue

            user.profile.member_type = socio_staff
            user.profile.is_on_roster = True # Asumimos que el staff está en la lista oficial
            user.profile.save()

            # Asignamos al staff a una o dos categorías al azar
            num_roles = random.randint(1, 2)
            for _ in range(num_roles):
                Role.objects.create(
                    profile=user.profile,
                    function='STA',
                    category=random.choice(categorias),
                    specific_position=random.choice(posiciones_staff)
                )

        self.stdout.write(self.style.SUCCESS('25 miembros del staff creados con éxito.'))