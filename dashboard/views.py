from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from members.models import Profile
from django.db import models

# Esta función comprueba si el usuario es un superusuario.
def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def dashboard_home(request):
    """
    Vista principal del Panel de Administración.
    Visible solo para superusuarios.
    """
    # Por ahora, solo renderizamos la plantilla.
    # Más adelante, aquí obtendremos los datos (pagos pendientes, etc.).
    context = {}
    return render(request, 'dashboard/dashboard.html', context)

@user_passes_test(is_superuser)
def member_list_view(request):
    """
    Muestra una lista de todos los socios con opciones de búsqueda y filtro.
    """
    profiles = Profile.objects.select_related('user').all()

    # Lógica de Búsqueda
    query = request.GET.get('q')
    if query:
        profiles = profiles.filter(
            models.Q(user__first_name__icontains=query) |
            models.Q(user__last_name__icontains=query) |
            models.Q(dni__icontains=query)
        ).distinct()

    context = {
        'profiles': profiles,
    }
    return render(request, 'dashboard/member_list.html', context)