from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import MembershipApplicationForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile, Role

# --- Vistas de Gestión de Socios ---

def membership_application(request):
    """Procesa el formulario de 'Quiero ser Socio' y envía un email al admin."""
    if request.method == 'POST':
        form = MembershipApplicationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            subject = f"Nueva Solicitud de Socio: {data['first_name']} {data['last_name']}"
            message_body = f"""
            Datos del aspirante:
            -------------------
            Nombre: {data['first_name']} {data['last_name']}
            Email: {data['email']}
            Teléfono: {data['phone_number']}
            Fecha de Nac.: {data.get('date_of_birth', 'No especificada')}
            Comentarios: {data.get('comments', 'Ninguno')}
            """
            send_mail(subject, message_body, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
            messages.success(request, '¡Tu solicitud ha sido enviada con éxito! Nos pondremos en contacto contigo a la brevedad.')
            return redirect('home')
    else:
        form = MembershipApplicationForm()
    return render(request, 'members/membership_application.html', {'form': form})

@login_required
def profile(request):
    """Muestra y actualiza el perfil del socio logueado."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tus datos han sido actualizados!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'members/profile.html', context)

# --- Vistas para el Plantel Público (movidas de la app 'players') ---

def player_list(request):
    """Muestra la lista pública del plantel, agrupada por función."""
    # Buscamos perfiles que sean Jugadores o Staff y estén en la lista oficial
    profiles_on_roster = Profile.objects.filter(is_on_roster=True)
    
    # Obtenemos los roles de esos perfiles para agruparlos
    roles = Role.objects.filter(profile__in=profiles_on_roster).order_by('function', 'specific_position')

    grouped_roles = {}
    for role in roles:
        function_display = role.get_function_display()
        if function_display not in grouped_roles:
            grouped_roles[function_display] = []
        grouped_roles[function_display].append(role)

    context = {'grouped_roles': grouped_roles}
    return render(request, 'members/player_list.html', context)

def player_detail(request, pk):
    """Muestra la ficha individual de un jugador o miembro del staff."""
    profile = Profile.objects.get(pk=pk)
    context = {'profile': profile}
    return render(request, 'members/player_detail.html', context)

# --- Vistas para Páginas Informativas ---

def benefits(request):
    return render(request, 'members/benefits.html')

def costs(request):
    return render(request, 'members/costs.html')

def code_of_conduct(request):
    return render(request, 'members/code_of_conduct.html')

def faq(request):
    return render(request, 'members/faq.html')