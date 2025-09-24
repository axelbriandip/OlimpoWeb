from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from collections import OrderedDict

# Importamos los modelos y formularios necesarios
from .models import Profile, Role, Category
from .forms import MembershipApplicationForm, UserUpdateForm, ProfileUpdateForm
from billing.forms import ReceiptUploadForm
from billing.models import Invoice

# --- Vistas del Plantel Público ---
def player_list(request):
    """
    Muestra la lista pública del plantel, con un filtro opcional por categoría.
    """
    profiles_on_roster = Profile.objects.filter(is_on_roster=True)
    roles = Role.objects.filter(profile__in=profiles_on_roster).select_related('profile', 'category', 'specific_position')

    # --- LÓGICA DE FILTRO ---
    category_filter_id = request.GET.get('category')
    if category_filter_id:
        roles = roles.filter(category__id=category_filter_id)

    # ... (la lógica de agrupación no cambia) ...
    grouped_players = OrderedDict()
    position_map = OrderedDict([
        ('Arqueros', ['Arquero']),
        ('Defensores', ['Defensor']),
        ('Mediocampistas', ['Mediocampista']),
        ('Delanteros', ['Delantero']),
        ('Cuerpo Técnico', ['Director Técnico', 'Ayudante de Campo', 'Preparador Físico'])
    ])

    for group_title, positions_in_group in position_map.items():
        roles_in_group = [
            role for role in roles if role.specific_position.name in positions_in_group
        ]
        if roles_in_group:
            grouped_players[group_title] = sorted(roles_in_group, key=lambda r: r.profile.user.last_name)
    
    context = {
        'grouped_players': grouped_players,
        'categories': Category.objects.all(), # Enviamos todas las categorías para los botones
        'selected_category_id': category_filter_id,
    }
    return render(request, 'members/player_list.html', context)
def player_detail(request, pk):
    """
    Muestra la ficha individual de un jugador o miembro del staff.
    """
    profile = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile}
    return render(request, 'members/player_detail.html', context)


# --- Vistas de Gestión de Socios ---

def membership_application(request):
    """
    Procesa el formulario de 'Quiero ser Socio' y envía un email al admin.
    """
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
    """
    Muestra y actualiza el perfil del socio logueado y su estado de cuenta.
    """
    if request.method == 'POST':
        # Verificamos si se está actualizando el perfil
        if 'update_profile' in request.POST:
            u_form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, '¡Tus datos han sido actualizados!')
                return redirect('profile')
        
        # Verificamos si se está subiendo un comprobante
        elif 'upload_receipt' in request.POST:
            invoice_id = request.POST.get('invoice_id')
            try:
                invoice = Invoice.objects.get(id=invoice_id, profile=request.user.profile)
                receipt_form = ReceiptUploadForm(request.POST, request.FILES)
                if receipt_form.is_valid():
                    payment = receipt_form.save(commit=False)
                    payment.invoice = invoice
                    payment.save()
                    invoice.status = 'VER' # Cambia a 'En Verificación'
                    invoice.save()
                    messages.success(request, '¡Comprobante recibido! Tu pago está siendo verificado.')
                else:
                    messages.error(request, 'Hubo un error al subir el comprobante.')
            except Invoice.DoesNotExist:
                messages.error(request, 'La factura no existe o no te pertenece.')
            return redirect('profile')

    # Para peticiones GET, preparamos los formularios
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    receipt_form = ReceiptUploadForm()
    
    # Obtenemos la cuenta corriente del socio
    invoices = request.user.profile.invoices.all()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'receipt_form': receipt_form,
        'invoices': invoices,
    }
    return render(request, 'members/profile.html', context)


# --- Vistas para Páginas Informativas ---

def benefits(request):
    return render(request, 'members/benefits.html')

def costs(request):
    return render(request, 'members/costs.html')

def code_of_conduct(request):
    return render(request, 'members/code_of_conduct.html')

def faq(request):
    return render(request, 'members/faq.html')
