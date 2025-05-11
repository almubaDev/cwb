from django import forms
from .models import Course, Module, Week, Session, VideoClass

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'version', 'description', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ['course', 'title', 'objectives', 'order']
        widgets = {
            'course': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'objectives': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class WeekForm(forms.ModelForm):
    class Meta:
        model = Week
        fields = ['module', 'title', 'description', 'order']
        widgets = {
            'module': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['week', 'title', 'order']
        widgets = {
            'week': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        
        
class VideoClassForm(forms.ModelForm):
    class Meta:
        model = VideoClass
        fields = [
            'session', 'title', 'description', 'video_url', 'duration', 
            'transcript', 'slides_url', 'is_external', 'thumbnail', 
            'order', 'is_visible', 'is_mandatory', 'tags', 
            'difficulty_level', 'is_evaluable', 'available_from', 
            'available_until', 'duration_minutes'
        ]
        widgets = {
            'session': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'video_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://www.youtube.com/watch?v=...'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Duración en segundos'}),
            'transcript': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'slides_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://docs.google.com/presentation/...'}),
            'is_external': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'python, django, html'}),
            'difficulty_level': forms.Select(attrs={'class': 'form-select'}),
            'is_evaluable': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'available_from': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'available_until': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tiempo estimado en minutos'})
        }
        help_texts = {
            'video_url': 'URL del video de YouTube, Vimeo u otra plataforma.',
            'duration': 'Duración del video en segundos.',
            'transcript': 'Transcripción textual completa del video.',
            'is_external': 'Marcar si el video está alojado en una plataforma externa.',
            'available_from': 'Fecha y hora a partir de la cual este video estará disponible.',
            'available_until': 'Fecha y hora hasta la cual este video estará disponible.',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer que algunos campos no sean requeridos
        self.fields['transcript'].required = False
        self.fields['slides_url'].required = False
        self.fields['thumbnail'].required = False
        self.fields['available_from'].required = False
        self.fields['available_until'].required = False
        self.fields['tags'].required = False
        
        # Añadir validación de JavaScript para convertir formato de tiempo HH:MM:SS a segundos
        self.fields['duration'].widget.attrs.update({
            'onchange': 'if(this.value.includes(":")) { this.value = convertTimeToSeconds(this.value); }',
        })