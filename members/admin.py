from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile

# Define un 'inline' para el modelo Profile
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfiles'

# Define un nuevo UserAdmin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-registra el admin de User con nuestra versión mejorada
admin.site.unregister(User)
admin.site.register(User, UserAdmin)