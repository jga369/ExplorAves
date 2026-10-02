from django.contrib import admin
from django.utils.html import format_html # Permite mostrar contenido HTML seguro dentro de Django Admin.

from .models import (
    Region,
    Departamento,
    Ave,
    ImagenAve,
    DistribucionAve,
    Migracion,
    PistaAve,
    PerfilJugador,
    ColeccionUsuario,
    ConfiguracionPartida,
    Partida,
    Pregunta,
    OpcionRespuesta,
    RespuestaJugador,
    AyudaUsada,
    Ranking,
    Logro,
    UsuarioLogro,
)

# ============================================================
# ADMINISTRACIÓN DE REGIONES
# ============================================================

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):

    # Columnas que aparecerán en el listado de regiones.
    list_display = (
        "id",
        "nombre",
    )

    # Permite buscar una región escribiendo su nombre.
    search_fields = (
        "nombre",
    )

    # Ordena las regiones alfabéticamente por nombre.
    ordering = (
        "nombre",
    )


# ============================================================
# ADMINISTRACIÓN DE DEPARTAMENTOS
# ============================================================

@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):

    # Columnas que aparecerán en el listado de departamentos.
    list_display = (
        "id",
        "nombre",
    )

    # Permite buscar departamentos por su nombre.
    search_fields = (
        "nombre",
    )

    # Agrega un filtro lateral utilizando las regiones.
    list_filter = (
        "regiones",
    )

    # Ordena los departamentos alfabéticamente.
    ordering = (
        "nombre",
    )

    # Hace más cómoda la selección de varias regiones.
    # En lugar de la caja básica de selección múltiple,
    # Django mostrará dos paneles para mover regiones
    # disponibles y seleccionadas.
    filter_horizontal = (
        "regiones",
    )
    
# ============================================================
# IMÁGENES DENTRO DEL FORMULARIO DE AVE
# ============================================================

class ImagenAveInline(admin.TabularInline):

    # Modelo relacionado que vamos a mostrar dentro de Ave.
    model = ImagenAve


    # Cantidad de formularios vacíos disponibles.
    extra = 3


    # Campos que se mostrarán.
    fields = (
        "imagen",
        "descripcion",
        "orden",
    )
    
# ============================================================
# ADMINISTRACIÓN DE AVES
# ============================================================

@admin.register(Ave)
class AveAdmin(admin.ModelAdmin):

        # Muestra el nombre científico en letra cursiva
    # sin modificar el valor almacenado en la base de datos.
    @admin.display(description="Nombre científico", ordering="nombre_cientifico")
    def nombre_cientifico_cursiva(self, obj):
        return format_html("<i>{}</i>", obj.nombre_cientifico)

    # Columnas visibles en la lista de aves.
    # Esto nos permitirá revisar rápidamente la información.
    list_display = (
        "id",
        "nombre_ingles",
        "nombre_cientifico_cursiva",
        "nombre_espanol",
        "es_migratoria",
    )


    # Campos donde funcionará el buscador.
    # Útil cuando tengamos cientos o miles de especies.
    search_fields = (
        "nombre_ingles",
        "nombre_cientifico",
        "nombre_espanol",
    )


    # Filtros laterales.
    # Permiten filtrar rápidamente las aves.
    list_filter = (
        "es_migratoria",
    )


    # Orden inicial de la tabla.
    ordering = (
        "nombre_ingles",
    )


    # Cantidad de registros por página.
    list_per_page = 25
    
# Agregar imágenes directamente al crear un ave.
    inlines = [
        ImagenAveInline,
    ]
    
    
admin.site.register(ImagenAve)
admin.site.register(DistribucionAve)
admin.site.register(Migracion)
admin.site.register(PistaAve)
admin.site.register(PerfilJugador)
admin.site.register(ColeccionUsuario)
admin.site.register(ConfiguracionPartida)
admin.site.register(Partida)
admin.site.register(Pregunta)
admin.site.register(OpcionRespuesta)
admin.site.register(RespuestaJugador)
admin.site.register(AyudaUsada)
admin.site.register(Ranking)
admin.site.register(Logro)
admin.site.register(UsuarioLogro)
