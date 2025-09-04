from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, MemberType, Role, Category

# --- Inlines para una gestión más cómoda ---

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)

class RoleInline(admin.TabularInline):
    """Permite añadir/editar roles directamente desde la página del Perfil."""
    model = Role
    extra = 1 # Muestra un campo para un nuevo rol por defecto.
    autocomplete_fields = ('category',)

class ProfileInline(admin.StackedInline):
    """Muestra el Perfil dentro de la página de edición del Usuario."""
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil de Socio'

# --- Admins de los modelos principales ---

@admin.register(MemberType)
class MemberTypeAdmin(admin.ModelAdmin):
    """Admin para los Tipos de Socio."""
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'member_type', 'dni') # Añadimos el nombre completo a la lista
    list_filter = ('member_type',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'dni')
    inlines = [RoleInline] # Mantenemos los roles aquí para una gestión clara
    
    # --- NUEVO: Mostramos campos del User como "solo lectura" ---
    readonly_fields = ('get_full_name', 'get_email', 'member_id')

    fieldsets = (
        ('Cuenta de Usuario', {
            'fields': ('user', 'get_full_name', 'get_email')
        }),
        ('Información del Perfil', {
            'fields': ('member_type', 'dni', 'date_of_birth', 'address', 'phone_number')
        }),
        ('Fotos', {
            'fields': ('profile_photo', 'extra_photo_1', 'extra_photo_2', 'dni_photo_front', 'dni_photo_back')
        }),
        ('Estados y Permisos', {
            'fields': ('is_on_roster', 'is_exempt')
        }),
    )

    # Funciones para obtener los datos del modelo User relacionado
    @admin.display(description='Nombre Completo')
    def get_full_name(self, obj):
        return obj.user.get_full_name()

    @admin.display(description='Email')
    def get_email(self, obj):
        return obj.user.email

class UserAdmin(BaseUserAdmin):
    """Extendemos el admin de User para incluir el Perfil."""
    inlines = (ProfileInline,)

# Re-registramos el admin de User con nuestra versión mejorada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)