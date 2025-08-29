from django import template
from django.utils import timezone

register = template.Library()

@register.filter(name='venue_display')
def venue_display(fixture):
    """
    Devuelve el lugar del partido o 'Lugar a confirmar' si no está definido.
    """
    if fixture.venue:
        return f", {fixture.venue}"

    # Si no hay lugar definido, mostramos 'a confirmar' para partidos de hoy o futuros
    if fixture.match_datetime.date() >= timezone.now().date():
        return ", Lugar a confirmar"

    # Si el partido ya pasó y no se cargó el lugar, no muestra nada
    return ""