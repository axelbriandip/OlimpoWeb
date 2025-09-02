from django.contrib import admin
from django.urls import path, include

# Necesario para servir archivos de medios (fotos) en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('players/', include('players.urls')),
    path('news/', include('news.urls')),
    path('fixtures/', include('fixtures.urls')),
    path('gallery/', include('gallery.urls')),
    path('members/', include('members.urls')),
]

# Esta línea es crucial para que se vean las fotos de los jugadores
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)