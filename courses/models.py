from django.db import models
from django.utils import timezone
from django.urls import reverse
from users.models import CustomUser


class Course(models.Model):
    """Modelo para representar un curso completo"""
    title = models.CharField(max_length=200, verbose_name="Título")
    version = models.CharField(max_length=50, verbose_name="Versión")
    description = models.TextField(verbose_name="Descripción")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos"
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.title} (v{self.version})"
    
    def get_absolute_url(self):
        return reverse('courses:course_detail', args=[self.id])


class Module(models.Model):
    """Modelo para representar un módulo dentro de un curso"""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules', 
                              verbose_name="Curso")
    title = models.CharField(max_length=200, verbose_name="Título")
    objectives = models.TextField(verbose_name="Objetivos")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.course.title} - Módulo {self.order}: {self.title}"


class Week(models.Model):
    """Modelo para representar una semana dentro de un módulo"""
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='weeks',
                              verbose_name="Módulo")
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Semana"
        verbose_name_plural = "Semanas"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.module.title} - Semana {self.order}: {self.title}"


class Session(models.Model):
    """Modelo para representar una sesión dentro de una semana"""
    week = models.ForeignKey(Week, on_delete=models.CASCADE, related_name='sessions',                  verbose_name="Semana")
    title = models.CharField(max_length=200, verbose_name="Título")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        verbose_name = "Sesión"
        verbose_name_plural = "Sesiones"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.week.title} - Sesión {self.order}: {self.title}"


class ContentItem(models.Model):
    """Modelo abstracto base para todos los tipos de contenido de sesiones"""
    
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='contents', verbose_name="Sesión")
    title = models.CharField(max_length=200, verbose_name="Título")
    order = models.PositiveIntegerField(default=0, verbose_name="Orden")
    is_visible = models.BooleanField(default=True, verbose_name="Visible para estudiantes")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="created_contents", verbose_name="Creado por")
    description = models.TextField(blank=True, verbose_name="Descripción")
    metadata = models.JSONField(default=dict, blank=True, verbose_name="Metadatos adicionales")
    duration_minutes = models.PositiveIntegerField(default=0, verbose_name="Duración estimada (minutos)",help_text="Tiempo estimado para completar este contenido")
    is_mandatory = models.BooleanField(default=True,verbose_name="Es obligatorio", help_text="Indica si este contenido es esencial para la sesión")
    
    # Campos opcionales
    available_from = models.DateTimeField(null=True, blank=True, verbose_name="Disponible desde", help_text="Fecha a partir de la cual este contenido estará disponible")
    available_until = models.DateTimeField(null=True, blank=True, verbose_name="Disponible hasta",help_text="Fecha hasta la cual este contenido estará disponible")
    tags = models.CharField(max_length=255, blank=True, verbose_name="Etiquetas", help_text="Etiquetas separadas por comas para categorizar el contenido")
    difficulty_level = models.CharField(max_length=20,
                                     choices=[
                                         ('beginner', 'Principiante'),
                                         ('intermediate', 'Intermedio'),
                                         ('advanced', 'Avanzado')
                                     ],default='beginner', verbose_name="Nivel de dificultad")
    is_evaluable = models.BooleanField(default=False, verbose_name="Es evaluable", help_text="Indica si este contenido contribuye a la evaluación")
    
    class Meta:
        abstract = True
        ordering = ['order']
        verbose_name = "Contenido"
        verbose_name_plural = "Contenidos"
        constraints = [
            models.UniqueConstraint(fields=['session', 'order'], name='%(app_label)s_%(class)s_unique_order_per_session')
        ]
    
    def __str__(self):
        return f"{self.title} (Sesión: {self.session.title})"
    
    def get_absolute_url(self):
        """Se debe implementar en las subclases"""
        raise NotImplementedError("Las subclases deben implementar este método")
    
    def get_content_type(self):
        """Devuelve el tipo de contenido basado en la subclase"""
        return self.__class__.__name__
    
    def is_available(self):
        """Comprueba si el contenido está disponible según las fechas programadas"""
        from django.utils import timezone
        now = timezone.now()
        
        # Si no hay restricciones de fechas, está disponible
        if not self.available_from and not self.available_until:
            return True
            
        # Comprobar restricciones de fecha de inicio
        if self.available_from and now < self.available_from:
            return False
            
        # Comprobar restricciones de fecha de fin
        if self.available_until and now > self.available_until:
            return False
            
        return True
    
    def is_completed_by(self, user):
        """Verifica si un usuario ha completado este contenido"""
        # Esto debe implementarse en subclases o usando un modelo ContentProgress
        return False
    
    def get_next_content(self):
        """Obtiene el siguiente contenido en la sesión basado en el orden"""
        return self.session.contents.filter(order__gt=self.order).order_by('order').first()
    
    def get_previous_content(self):
        """Obtiene el contenido anterior en la sesión basado en el orden"""
        return self.session.contents.filter(order__lt=self.order).order_by('-order').first()
    
    

class VideoClass(ContentItem):
    """Modelo para representar una clase en video"""
    
    video_url = models.URLField(
        verbose_name="URL del video",
        help_text="URL del video (YouTube, Vimeo, etc.)"
    )
    duration = models.PositiveIntegerField(
        verbose_name="Duración (segundos)",
        help_text="Duración del video en segundos",
        default=0
    )
    transcript = models.TextField(
        verbose_name="Transcripción",
        blank=True,
        help_text="Transcripción textual del contenido del video"
    )
    slides_url = models.URLField(
        verbose_name="URL de diapositivas",
        blank=True,
        help_text="URL de las diapositivas utilizadas en el video (Google Slides, PDF, etc.)"
    )
    is_external = models.BooleanField(
        default=True,
        verbose_name="Video externo",
        help_text="Indica si el video está alojado en una plataforma externa o en el servidor"
    )
    thumbnail = models.ImageField(
        upload_to='video_thumbnails/',
        blank=True,
        null=True,
        verbose_name="Miniatura",
        help_text="Imagen de vista previa del video"
    )
    
    class Meta:
        verbose_name = "Video Clase"
        verbose_name_plural = "Video Clases"
        ordering = ['session', 'order']
    
    def get_absolute_url(self):
        """Retorna la URL para acceder a los detalles del video"""
        return reverse('courses:video_detail', args=[self.id])
    
    def get_embed_url(self):
        """
        Obtiene la URL para insertar el video según la plataforma
        (YouTube, Vimeo, etc.)
        """
        url = self.video_url.lower()
        
        # YouTube
        if 'youtube.com' in url or 'youtu.be' in url:
            if 'youtube.com/watch' in url:
                # Formato: https://www.youtube.com/watch?v=VIDEO_ID
                video_id = url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                # Formato: https://youtu.be/VIDEO_ID
                video_id = url.split('youtu.be/')[1].split('?')[0]
            else:
                return url
                
            return f"https://www.youtube.com/embed/{video_id}"
            
        # Vimeo
        elif 'vimeo.com' in url:
            # Formato: https://vimeo.com/VIDEO_ID
            try:
                video_id = url.split('vimeo.com/')[1].split('?')[0]
                return f"https://player.vimeo.com/video/{video_id}"
            except IndexError:
                return url
                
        # Otros tipos de videos - retornar la URL original
        return url
    
    def video_platform(self):
        """Determina la plataforma del video basado en la URL"""
        url = self.video_url.lower()
        
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'YouTube'
        elif 'vimeo.com' in url:
            return 'Vimeo'
        elif 'loom.com' in url:
            return 'Loom'
        else:
            return 'Otro'