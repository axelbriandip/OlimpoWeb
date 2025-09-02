from django import forms
from django.contrib.auth.models import User
from .models import Profile, Payment

class UserRegisterForm(forms.ModelForm):
    """
    Formulario para el registro de nuevos usuarios (socios).
    """
    # --- Campos para el modelo User ---
    # Hacemos que la contraseña use un widget de tipo password
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirmar Contraseña")

    # --- Campos para el modelo Profile ---
    dni = forms.CharField(max_length=20, label="DNI")
    address = forms.CharField(max_length=255, label="Dirección")
    phone_number = forms.CharField(max_length=50, label="Teléfono")

    class Meta:
        model = User
        # Campos del modelo User que queremos en el formulario
        fields = ['first_name', 'last_name', 'email', 'username']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'username': 'Nombre de Usuario',
        }

    def clean_password_confirm(self):
        """
        Validación para asegurar que las dos contraseñas coincidan.
        """
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        
        return password_confirm

class UserUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos del modelo User."""
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
        }

class ProfileUpdateForm(forms.ModelForm):
    """Formulario para actualizar datos del modelo Profile."""
    class Meta:
        model = Profile
        fields = ['dni', 'address', 'phone_number']
        labels = {
            'dni': 'DNI',
            'address': 'Dirección',
            'phone_number': 'Teléfono',
        }

class ReceiptUploadForm(forms.ModelForm):
    """
    Formulario para que el socio suba su comprobante de pago.
    """
    class Meta:
        model = Payment
        fields = ['receipt']
        labels = {
            'receipt': 'Adjuntar comprobante (captura de pantalla o foto)',
        }