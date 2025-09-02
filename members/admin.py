from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Membership

# --- AÑADE ESTA NUEVA CLASE ---
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'dni', 'phone_number')
    # Habilitamos la búsqueda para que el autocomplete en Membership funcione
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'dni')

# 1. El inline para Profile se mantiene igual
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfiles'

# 2. El UserAdmin vuelve a tener solo el ProfileInline
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# 3. Creamos un admin separado para la Membresía
@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('profile', 'status', 'last_payment_date', 'next_due_date')
    list_filter = ('status',)
    list_editable = ('status', 'last_payment_date', 'next_due_date')
    # Este campo de búsqueda te ayudará a encontrar socios fácilmente
    autocomplete_fields = ('profile',) 

# Re-registramos el admin de User como antes
admin.site.unregister(User)
admin.site.register(User, UserAdmin)