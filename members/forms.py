from django import forms
from .models import Role

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

class ProfileAdminUpdateForm(forms.ModelForm):
    """Formulario para editar los datos del Perfil desde el dashboard."""
    class Meta:
        model = Profile
        fields = [
            'member_type', 'date_of_birth', 'dni', 'address', 'phone_number', 
            'is_on_roster', 'is_exempt', 'profile_photo', 'extra_photo_1', 
            'extra_photo_2', 'dni_photo_front', 'dni_photo_back'
        ]

class RoleForm(forms.ModelForm):
    """Formulario para un único Rol."""
    class Meta:
        model = Role
        fields = ['function', 'category', 'specific_position']

class MemberCreationForm(forms.ModelForm):
    """Formulario para crear un nuevo User y Profile desde el dashboard."""
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña Inicial")
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': 'Nombre de Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }