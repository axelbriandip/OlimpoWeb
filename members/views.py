from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Profile, Membership
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, ReceiptUploadForm, UserRegisterForm
from datetime import date
from dateutil.relativedelta import relativedelta

def register(request):
    """
    Gestiona el registro de nuevos socios.
    """
    if request.method == 'POST':
        # Si el formulario se envió, lo procesamos
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # 1. Creamos el objeto User pero no lo guardamos todavía
            user = form.save(commit=False)
            # 2. Hasheamos la contraseña
            user.set_password(form.cleaned_data['password'])
            # 3. Ahora sí, guardamos el User
            user.save()
            
            # 4. Creamos el Perfil asociado al nuevo usuario
            Profile.objects.create(
                user=user,
                dni=form.cleaned_data['dni'],
                address=form.cleaned_data['address'],
                phone_number=form.cleaned_data['phone_number']
            )
            
            # Mostramos un mensaje de éxito y redirigimos al inicio
            messages.success(request, f'¡Tu cuenta ha sido creada exitosamente! Ya puedes iniciar sesión.')
            return redirect('home')
    else:
        # Si se visita la página por primera vez, mostramos un formulario vacío
        form = UserRegisterForm()
        
    return render(request, 'members/register.html', {'form': form})

@login_required
def profile(request):
    """
    Gestiona la visualización, actualización de datos y subida de comprobantes.
    """
        # Se asegura de que el perfil del usuario tenga un objeto de membresía asociado.
    # Si no existe, lo crea. Si ya existe, simplemente lo obtiene.
    Membership.objects.get_or_create(profile=request.user.profile)

    if request.method == 'POST':
        # Verificamos qué formulario se está enviando
        if 'update_profile' in request.POST:
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, '¡Tus datos han sido actualizados!')
                return redirect('profile')
        
        elif 'upload_receipt' in request.POST:
            receipt_form = ReceiptUploadForm(request.POST, request.FILES)
            if receipt_form.is_valid():
                payment = receipt_form.save(commit=False)
                payment.profile = request.user.profile
                payment.save() # Al guardar, la fecha se añade sola

                # --- LÓGICA DE ACTUALIZACIÓN AUTOMÁTICA ---
                membership = request.user.profile.membership
                
                # Usamos la fecha que se guardó automáticamente en el objeto 'payment'
                membership.status = 'ACT'
                membership.last_payment_date = payment.payment_date
                membership.next_due_date = payment.payment_date + relativedelta(months=+1)
                membership.save()

                messages.success(request, '¡Comprobante recibido! Tu estado de cuenta ha sido actualizado. Gracias por tu pago.')
                return redirect('profile')

    # Si se visita la página (GET), mostramos todos los formularios vacíos
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    receipt_form = ReceiptUploadForm()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'receipt_form': receipt_form
    }

    return render(request, 'members/profile.html', context)

def code_of_conduct(request):
    """
    Muestra la página del Código de Conducta.
    """
    return render(request, 'members/code_of_conduct.html')

def faq(request):
    """
    Muestra la página de Preguntas Frecuentes.
    """
    return render(request, 'members/faq.html')

def benefits(request):
    """
    Muestra la página de beneficios para socios.
    """
    return render(request, 'members/benefits.html')

def costs(request):
    """
    Muestra la página de costos y categorías de socios.
    """
    return render(request, 'members/costs.html')