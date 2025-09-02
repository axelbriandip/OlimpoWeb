from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

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
    Gestiona la visualización y actualización del perfil del socio.
    """
    if request.method == 'POST':
        # Si se envía el formulario, procesamos los datos
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, '¡Tu perfil ha sido actualizado con éxito!')
            return redirect('profile') # Redirigimos a la misma página

    else:
        # Si se visita la página, mostramos los formularios con los datos actuales
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
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