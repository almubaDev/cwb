from django.db import models
from django.urls import reverse
from django.conf import settings
from courses.models import Session, ContentItem

class CodeReading(ContentItem):
    """
    Modelo principal para Lectura de Código. Extiende ContentItem para
    integrarse con el sistema de contenidos existente.
    """
    title = models.CharField(
        max_length=255, 
        verbose_name="Título"
    )
    description = models.TextField(
        verbose_name="Descripción",
        blank=True
    )
    PROGRAMMING_LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('java', 'Java'),
        ('csharp', 'C#'),
        ('cpp', 'C++'),
        ('php', 'PHP'),
        ('ruby', 'Ruby'),
        ('go', 'Go'),
        ('swift', 'Swift'),
        ('typescript', 'TypeScript'),
        ('html', 'HTML'),
        ('css', 'CSS'),
        ('sql', 'SQL'),
        ('bash', 'Bash/Shell'),
        ('other', 'Otro'),
    ]
    programming_language = models.CharField(
        max_length=50,
        verbose_name="Lenguaje de Programación",
        choices=PROGRAMMING_LANGUAGE_CHOICES,
        default="python",
        help_text="Lenguaje de programación principal del código"
    )
    session = models.ForeignKey(
        Session, 
        on_delete=models.CASCADE,
        related_name='code_readings',
        verbose_name="Sesión"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Orden"
    )
    is_visible = models.BooleanField(
        default=True,
        verbose_name="Visible para estudiantes"
    )
    is_mandatory = models.BooleanField(
        default=False,
        verbose_name="Es obligatorio"
    )
    is_evaluable = models.BooleanField(
        default=False,
        verbose_name="Es evaluable"
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_code_readings',
        verbose_name="Creado por"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Lectura de Código"
        verbose_name_plural = "Lecturas de Código"
        ordering = ['session', 'order']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('code_reading:codereading_detail', args=[self.id])
    
    def get_steps_count(self):
        return self.steps.count()


class CodeReadingStep(models.Model):
    """
    Representa un paso o sección dentro de una lectura de código.
    Cada paso puede tener múltiples bloques de código y explicaciones.
    """
    code_reading = models.ForeignKey(
        CodeReading,
        on_delete=models.CASCADE,
        related_name='steps',
        verbose_name="Lectura de Código"
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Título del paso"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Orden"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción general del paso"
    )
    
    class Meta:
        verbose_name = "Paso de Lectura"
        verbose_name_plural = "Pasos de Lectura"
        ordering = ['code_reading', 'order']
    
    def __str__(self):
        return f"{self.code_reading.title} - Paso {self.order}: {self.title}"


class CodeBlock(models.Model):
    """
    Representa un bloque de código que se mostrará en la parte izquierda.
    """
    step = models.ForeignKey(
        CodeReadingStep,
        on_delete=models.CASCADE,
        related_name='code_blocks',
        verbose_name="Paso"
    )
    code = models.TextField(
        verbose_name="Código"
    )
    language = models.CharField(
        max_length=50,
        verbose_name="Lenguaje",
        default="python"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Orden"
    )
    highlight_lines = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Líneas a resaltar",
        help_text="Formato: '1,3,5-7' para resaltar líneas 1, 3, y del 5 al 7"
    )
    
    class Meta:
        verbose_name = "Bloque de Código"
        verbose_name_plural = "Bloques de Código"
        ordering = ['step', 'order']
    
    def __str__(self):
        return f"Código {self.order} - {self.step}"


class ExplanationBlock(models.Model):
    """
    Representa un bloque de explicación que se mostrará en la parte derecha.
    """
    step = models.ForeignKey(
        CodeReadingStep,
        on_delete=models.CASCADE,
        related_name='explanation_blocks',
        verbose_name="Paso"
    )
    content = models.TextField(
        verbose_name="Contenido de la explicación"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Orden"
    )
    related_code_block = models.ForeignKey(
        CodeBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='explanations',
        verbose_name="Bloque de código relacionado"
    )
    
    class Meta:
        verbose_name = "Bloque de Explicación"
        verbose_name_plural = "Bloques de Explicación"
        ordering = ['step', 'order']
    
    def __str__(self):
        return f"Explicación {self.order} - {self.step}"


class QuestionBlock(models.Model):
    """
    Representa una pregunta que el estudiante debe responder,
    ubicada en la parte derecha.
    """
    step = models.ForeignKey(
        CodeReadingStep,
        on_delete=models.CASCADE,
        related_name='question_blocks',
        verbose_name="Paso"
    )
    question_text = models.TextField(
        verbose_name="Texto de la pregunta"
    )
    correct_answer = models.TextField(
        verbose_name="Respuesta correcta",
        help_text="Para IA: criterios de la respuesta correcta"
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Orden"
    )
    related_code_block = models.ForeignKey(
        CodeBlock,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='questions',
        verbose_name="Bloque de código relacionado"
    )
    
    class Meta:
        verbose_name = "Bloque de Pregunta"
        verbose_name_plural = "Bloques de Pregunta"
        ordering = ['step', 'order']
    
    def __str__(self):
        return f"Pregunta {self.order} - {self.step}"


class StudentResponse(models.Model):
    """
    Almacena las respuestas de los estudiantes a las preguntas.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='code_reading_responses',
        verbose_name="Estudiante"
    )
    question = models.ForeignKey(
        QuestionBlock,
        on_delete=models.CASCADE,
        related_name='student_responses',
        verbose_name="Pregunta"
    )
    response_text = models.TextField(
        verbose_name="Respuesta del estudiante"
    )
    ai_feedback = models.TextField(
        blank=True,
        verbose_name="Feedback de la IA"
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )
    
    class Meta:
        verbose_name = "Respuesta de Estudiante"
        verbose_name_plural = "Respuestas de Estudiantes"
        unique_together = ['user', 'question']
    
    def __str__(self):
        return f"Respuesta de {self.user.username} a {self.question}"


class StudentProgress(models.Model):
    """
    Seguimiento del progreso del estudiante en una lectura de código.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='code_reading_progress',
        verbose_name="Estudiante"
    )
    code_reading = models.ForeignKey(
        CodeReading,
        on_delete=models.CASCADE,
        related_name='student_progress',
        verbose_name="Lectura de Código"
    )
    current_step = models.ForeignKey(
        CodeReadingStep,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_current',
        verbose_name="Paso actual"
    )
    completed_steps = models.ManyToManyField(
        CodeReadingStep,
        blank=True,
        related_name='student_completed',
        verbose_name="Pasos completados"
    )
    is_completed = models.BooleanField(
        default=False,
        verbose_name="¿Completado?"
    )
    started_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de inicio"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de finalización"
    )
    
    class Meta:
        verbose_name = "Progreso de Estudiante"
        verbose_name_plural = "Progresos de Estudiantes"
        unique_together = ['user', 'code_reading']
    
    def __str__(self):
        return f"Progreso de {self.user.username} en {self.code_reading.title}"
