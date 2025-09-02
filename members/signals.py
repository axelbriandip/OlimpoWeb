from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Membership

@receiver(post_save, sender=User)
def create_profile_and_membership(sender, instance, created, **kwargs):
    """
    Crea un Perfil y una Membresía automáticamente cada vez que se crea un nuevo usuario.
    """
    if created:
        profile = Profile.objects.create(user=instance)
        Membership.objects.create(profile=profile)