from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Membership

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'member_type', 'dni')
    list_filter = ('member_type',) # Permite filtrar por tipo de socio
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'dni')
    # Usamos un widget más cómodo para la selección de Vínculos
    filter_horizontal = ('linked_profiles',)

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfiles'
    # Hacemos que el campo de Vínculos sea más usable aquí también
    filter_horizontal = ('linked_profiles',)

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