from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User


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