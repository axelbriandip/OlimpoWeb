from django import forms

class MembershipApplicationForm(forms.Form):
    """Formulario para que un aspirante a socio envíe sus datos."""
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    email = forms.EmailField(label="Correo Electrónico")
    phone_number = forms.CharField(label="Teléfono de Contacto")
    date_of_birth = forms.DateField(
        label="Fecha de Nacimiento",
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    comments = forms.CharField(
        label="Comentarios (ej: categoría de interés)", 
        widget=forms.Textarea, 
        required=False
    )

# --- Formularios para el Perfil del Socio ---
from django.contrib.auth.models import User
from .models import Profile

class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos básicos del User."""
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = { 'first_name': 'Nombre', 'last_name': 'Apellido', 'email': 'Correo Electrónico' }

class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos del Profile."""
    class Meta:
        model = Profile
        fields = ['dni', 'address', 'phone_number', 'profile_photo']
        labels = { 
            'dni': 'DNI', 
            'address': 'Dirección', 
            'phone_number': 'Teléfono',
            'profile_photo': 'Foto de Perfil',
        }