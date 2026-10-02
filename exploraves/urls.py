# Administrador de Django.
from django.contrib import admin
# Sistema de URLs de Django.
from django.urls import path
# Nos permite acceder a la configuración MEDIA_URL y MEDIA_ROOT.
from django.conf import settings
# Permite servir los archivos multimedia durante el desarrollo.
from django.conf.urls.static import static


# ============================================================
# URLS PRINCIPALES DEL PROYECTO
# ============================================================

urlpatterns = [
    # Panel de administración.
    path('admin/', admin.site.urls),
]

# ============================================================
# ARCHIVOS MULTIMEDIA
# ============================================================

""" Durante el desarrollo, permite que Django muestre las imágenes
almacenadas dentro de la carpeta MEDIA_ROOT.
Por ejemplo:
media/aves/imagen.jpg
podrá visualizarse mediante:
/media/aves/imagen.jpg"""
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )