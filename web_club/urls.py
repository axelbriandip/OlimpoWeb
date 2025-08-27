from django.contrib import admin
from django.urls import path, include # ¡Asegúrate de importar 'include'!

# Necesario para servir archivos de medios (fotos) en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('players/', include('players.urls')), # Conecta las URLs de nuestra app
]

# Esta línea es crucial para que se vean las fotos de los jugadores
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)