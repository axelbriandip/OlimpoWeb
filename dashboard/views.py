from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

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