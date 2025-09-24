from django.core.management.base import BaseCommand
from django.core import management
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Runs all population scripts in the correct order.'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('--- Iniciando la populación completa ---'))
        
        # --- AÑADIMOS EL BORRADO PRINCIPAL AQUÍ ---
        self.stdout.write('Borrando datos antiguos (excepto superusuarios)...')
        User.objects.filter(is_superuser=False).delete()
        # Al borrar los Users, los Profiles y Roles se borran en cascada.
        # Esto libera las dependencias de los catálogos.
        self.stdout.write('Datos antiguos borrados.')

        # El orden es importante
        management.call_command('populate_catalogs') # Un script base para los catálogos
        management.call_command('populate_players')
        management.call_command('populate_staff')
        management.call_command('populate_board')
        management.call_command('populate_news')
        management.call_command('populate_fixtures')
        
        self.stdout.write(self.style.SUCCESS('--- Populación completa finalizada ---'))