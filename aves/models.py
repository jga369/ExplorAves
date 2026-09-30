from django.db import models
from django.contrib.auth.models import User


# ==========================================================
# UBICACIÓN GEOGRÁFICA DE LAS AVES
# ==========================================================


class Region(models.Model):
    """
    Regiones naturales de Colombia:

    - Andina
    - Caribe
    - Pacífica
    - Amazonía
    - Orinoquía

    Una región puede tener muchos departamentos.
    """

    nombre = models.CharField(
        max_length=100,
        unique=True
    )

    descripcion = models.TextField(
        blank=True
    )


    def __str__(self):
        return self.nombre



class Departamento(models.Model):
    """
    Departamentos de Colombia.

    Ejemplo:

    Cundinamarca -> Región Andina
    Amazonas -> Región Amazónica
    """

    nombre = models.CharField(
        max_length=100
    )


    region = models.ForeignKey(
        Region,
        related_name="departamentos",
        on_delete=models.CASCADE
    )


    def __str__(self):
        return self.nombre



# ==========================================================
# BANCO PRINCIPAL DE AVES
# ==========================================================


class Ave(models.Model):
    """
    Información principal de cada especie.

    Esta tabla será el corazón del juego.
    """

    nombre_ingles = models.CharField(
        max_length=150
    )


    nombre_cientifico = models.CharField(
        max_length=150,
        unique=True
    )


    nombre_espanol = models.CharField(
        max_length=150,
        blank=True
    )


    descripcion = models.TextField()


    nivel_dificultad = models.IntegerField(
        default=1
    )


    es_migratoria = models.BooleanField(
        default=False
    )


    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.nombre_ingles



class ImagenAve(models.Model):
    """
    Una especie puede tener varias imágenes.

    Ejemplo:

    Colibri coruscans

    Imagen 1
    Imagen 2
    Imagen 3

    Se usa para el carrusel del juego.
    """

    ave = models.ForeignKey(
        Ave,
        related_name="imagenes",
        on_delete=models.CASCADE
    )


    imagen = models.ImageField(
        upload_to="aves/"
    )


    descripcion = models.CharField(
        max_length=200,
        blank=True
    )


    orden = models.IntegerField(
        default=1
    )


    class Meta:

        ordering = [
            "orden"
        ]


    def __str__(self):
        return self.ave.nombre_ingles



# ==========================================================
# DISTRIBUCIÓN GEOGRÁFICA
# ==========================================================


class DistribucionAve(models.Model):
    """
    Relación entre aves y lugares.

    Una ave puede estar:

    - En una región
    - En varias regiones
    - En todo Colombia

    Ejemplo:

    Colibrí X:

    Andina
    Amazonía
    Orinoquía
    """

    ave = models.ForeignKey(
        Ave,
        related_name="distribuciones",
        on_delete=models.CASCADE
    )


    region = models.ForeignKey(
        Region,
        related_name="aves",
        on_delete=models.CASCADE
    )


    departamento = models.ForeignKey(
        Departamento,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "ave",
                    "region",
                    "departamento"
                ],
                name="distribucion_unica"
            )

        ]



# ==========================================================
# MIGRACIÓN
# ==========================================================


class Migracion(models.Model):
    """
    Información adicional para aves migratorias.
    """

    ave = models.OneToOneField(
        Ave,
        on_delete=models.CASCADE
    )


    origen = models.CharField(
        max_length=150
    )


    temporada_llegada = models.CharField(
        max_length=100
    )


    temporada_salida = models.CharField(
        max_length=100
    )


    ruta = models.TextField()


    def __str__(self):
        return self.ave.nombre_ingles



# ==========================================================
# PISTAS DEL JUEGO
# ==========================================================


class PistaAve(models.Model):
    """
    Pistas utilizadas durante una pregunta.

    Ejemplo:

    Nivel 1:
    "Tiene colores brillantes"

    Nivel 2:
    "Su pico es largo"

    Nivel 3:
    "Vive en zonas altas"
    """

    ave = models.ForeignKey(
        Ave,
        related_name="pistas",
        on_delete=models.CASCADE
    )


    texto = models.TextField()


    nivel = models.IntegerField(
        default=1
    )


    orden = models.IntegerField(
        default=1
    )


    class Meta:

        ordering = [
            "orden"
        ]
        
        
# ==========================================================
# USUARIOS Y PROGRESO DEL JUGADOR
# ==========================================================


class PerfilJugador(models.Model):
    """
    Información adicional del usuario.

    Django ya tiene la tabla User.
    Esta tabla guarda estadísticas del jugador.
    """

    usuario = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )


    nivel = models.IntegerField(
        default=1
    )


    experiencia = models.IntegerField(
        default=0
    )


    puntos_totales = models.IntegerField(
        default=0
    )


    partidas_jugadas = models.IntegerField(
        default=0
    )


    aves_identificadas = models.IntegerField(
        default=0
    )


    aciertos_totales = models.IntegerField(
        default=0
    )


    errores_totales = models.IntegerField(
        default=0
    )


    mejor_puntuacion = models.IntegerField(
        default=0
    )


    tiempo_promedio = models.FloatField(
        default=0
    )


    def __str__(self):
        return self.usuario.username




class ColeccionUsuario(models.Model):
    """
    Álbum personal del jugador.

    Guarda las aves que ya identificó.

    Ejemplo:

    Juan:

    ✓ Cóndor Andino
    ✓ Colibrí coruscans
    ✓ Tucán
    """

    usuario = models.ForeignKey(
        User,
        related_name="coleccion",
        on_delete=models.CASCADE
    )


    ave = models.ForeignKey(
        Ave,
        related_name="jugadores_que_identificaron",
        on_delete=models.CASCADE
    )


    fecha_identificacion = models.DateTimeField(
        auto_now_add=True
    )


    cantidad_identificaciones = models.IntegerField(
        default=1
    )


    mejor_tiempo = models.FloatField(
        default=0
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "usuario",
                    "ave"
                ],
                name="ave_identificada_usuario"
            )

        ]



# ==========================================================
# CONFIGURACIÓN DEL JUEGO
# ==========================================================


class ConfiguracionPartida(models.Model):
    """
    Configuraciones disponibles:

    Toda Colombia
    Regiones
    Migratorias

    Cantidad:

    10 preguntas
    25 preguntas
    50 preguntas
    100 preguntas
    """

    modo_juego = models.CharField(
        max_length=50
    )


    cantidad_preguntas = models.IntegerField()


    vidas = models.IntegerField()


    tiempo_por_pregunta = models.IntegerField(
        default=10
    )


    def __str__(self):
        return (
            f"{self.modo_juego} - "
            f"{self.cantidad_preguntas} preguntas"
        )



# ==========================================================
# PARTIDAS
# ==========================================================


class Partida(models.Model):
    """
    Guarda cada partida realizada.

    Ejemplo:

    Usuario:
    Juan

    Configuración:
    25 preguntas

    Resultado:
    3200 puntos
    """

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    configuracion = models.ForeignKey(
        ConfiguracionPartida,
        on_delete=models.CASCADE
    )


    vidas_iniciales = models.IntegerField()


    vidas_finales = models.IntegerField()


    puntos_finales = models.IntegerField(
        default=0
    )


    fecha_inicio = models.DateTimeField(
        auto_now_add=True
    )


    fecha_fin = models.DateTimeField(
        null=True,
        blank=True
    )


    def __str__(self):
        return f"Partida {self.id}"



# ==========================================================
# PREGUNTAS Y RESPUESTAS
# ==========================================================


class Pregunta(models.Model):
    """
    Cada tarjeta mostrada durante el juego.

    Contiene:

    - Ave correcta
    - Tiempo
    - Estado
    """

    partida = models.ForeignKey(
        Partida,
        related_name="preguntas",
        on_delete=models.CASCADE
    )


    ave_correcta = models.ForeignKey(
        Ave,
        on_delete=models.CASCADE
    )


    numero_pregunta = models.IntegerField()


    tiempo_limite = models.IntegerField(
        default=10
    )


    tiempo_utilizado = models.FloatField(
        null=True,
        blank=True
    )


    respondida = models.BooleanField(
        default=False
    )


    def __str__(self):
        return f"Pregunta {self.numero_pregunta}"




class OpcionRespuesta(models.Model):
    """
    Las 4 opciones mostradas.

    Ejemplo:

    A. Colibri coruscans
    B. Tucán
    C. Cóndor
    D. Águila
    """

    pregunta = models.ForeignKey(
        Pregunta,
        related_name="opciones",
        on_delete=models.CASCADE
    )


    ave = models.ForeignKey(
        Ave,
        related_name="opciones_respuesta",
        on_delete=models.CASCADE
    )


    es_correcta = models.BooleanField(
        default=False
    )


    orden = models.IntegerField()


    class Meta:

        ordering = [
            "orden"
        ]


    def __str__(self):
        return self.ave.nombre_ingles




class RespuestaJugador(models.Model):
    """
    Guarda la decisión del jugador.

    Sirve para estadísticas:

    - Aciertos
    - Errores
    - Tiempo
    - Puntos
    """

    pregunta = models.ForeignKey(
        Pregunta,
        related_name="respuestas",
        on_delete=models.CASCADE
    )


    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    opcion = models.ForeignKey(
        OpcionRespuesta,
        on_delete=models.CASCADE
    )


    correcta = models.BooleanField(
        default=False
    )


    tiempo_utilizado = models.FloatField()


    uso_ayuda = models.BooleanField(
        default=False
    )


    puntos_obtenidos = models.IntegerField(
        default=0
    )



# ==========================================================
# SISTEMA DE AYUDAS
# ==========================================================


class AyudaUsada(models.Model):
    """
    Ayudas disponibles:

    1. 50/50
    2. Cambiar pregunta
    3. Mostrar respuesta correcta

    Guarda la penalización aplicada.
    """

    partida = models.ForeignKey(
        Partida,
        related_name="ayudas",
        on_delete=models.CASCADE
    )


    pregunta = models.ForeignKey(
        Pregunta,
        related_name="ayudas",
        on_delete=models.CASCADE
    )


    TIPOS_AYUDA = (

        ("5050", "50/50"),

        ("cambiar", "Cambiar pregunta"),

        ("respuesta", "Mostrar respuesta"),

    )


    tipo = models.CharField(
        max_length=20,
        choices=TIPOS_AYUDA
    )


    penalizacion = models.IntegerField()


    descripcion = models.CharField(
        max_length=100,
        blank=True
    )


    fecha = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "pregunta",
                    "tipo"
                ],
                name="una_ayuda_por_tipo"
            )

        ]



# ==========================================================
# RANKING
# ==========================================================


class Ranking(models.Model):
    """
    Tabla de posiciones.

    Puede manejar:

    - Ranking semanal
    - Ranking mensual
    - Ranking histórico
    """

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    puntos = models.IntegerField(
        default=0
    )


    tipo_ranking = models.CharField(
        max_length=50
    )


    periodo = models.CharField(
        max_length=50
    )


    fecha = models.DateTimeField(
        auto_now_add=True
    )



# ==========================================================
# GAMIFICACIÓN
# ==========================================================


class Logro(models.Model):
    """
    Premios desbloqueables.

    Ejemplo:

    "Primeras 10 aves"

    "Experto colombiano"
    """

    nombre = models.CharField(
        max_length=100
    )


    descripcion = models.TextField()


    imagen = models.ImageField(
        upload_to="logros/",
        blank=True
    )


    def __str__(self):
        return self.nombre




class UsuarioLogro(models.Model):

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


    logro = models.ForeignKey(
        Logro,
        on_delete=models.CASCADE
    )


    fecha_obtenido = models.DateTimeField(
        auto_now_add=True
    )