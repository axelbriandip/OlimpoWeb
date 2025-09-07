from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Se asegura de que exista un Perfil para cada Usuario.
    Usa get_or_create para evitar errores si el perfil ya fue creado por otro medio.
    """
    if created:
        Profile.objects.get_or_create(user=instance)