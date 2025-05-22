# code_reading/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import (
    CodeReading, CodeReadingStep, CodeBlock, 
    ExplanationBlock, QuestionBlock, StudentResponse
)

# code_reading/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import (
    CodeReading, CodeReadingStep, CodeBlock, 
    ExplanationBlock, QuestionBlock, StudentResponse, StudentCodeSubmission
)

class CodeReadingForm(forms.ModelForm):
    """Formulario para crear y editar Lecturas de Código"""

    class Meta:
        model = CodeReading
        fields = [
            'title', 'description', 'programming_language', 
            'session', 'order', 'is_visible', 'is_mandatory', 'is_evaluable'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 4}),
            'programming_language': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'session': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'is_visible': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
            'is_mandatory': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
            'is_evaluable': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.pk:  # Si es nuevo objeto
            instance.created_by = self.user
        if commit:
            instance.save()
        return instance


class CodeReadingStepForm(forms.ModelForm):
    """Formulario para crear y editar Pasos de Lectura de Código"""

    class Meta:
        model = CodeReadingStep
        fields = ['code_reading', 'title', 'order', 'description']
        widgets = {
            'code_reading': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        code_reading = kwargs.pop('code_reading', None)
        super().__init__(*args, **kwargs)
        
        # Si se proporciona una lectura de código, preestablecerla y calcular el siguiente orden
        if code_reading:
            self.fields['code_reading'].initial = code_reading
            if not self.instance.pk:  # Si es un objeto nuevo
                next_order = CodeReadingStep.objects.filter(code_reading=code_reading).count() + 1
                self.fields['order'].initial = next_order


class CodeBlockForm(forms.ModelForm):
    """Formulario para crear y editar Bloques de Código"""

    class Meta:
        model = CodeBlock
        fields = [
            'step', 'code', 'language', 'order', 'highlight_lines',
            'is_editable', 'show_line_numbers', 'theme', 'height', 
            'wrap_lines', 'allow_student_submissions'
        ]
        widgets = {
            'step': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'code': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 font-mono', 
                'rows': 15,
                'placeholder': 'Escribe tu código aquí...',
                'style': 'font-family: "Courier New", Courier, monospace;'
            }),
            'language': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'highlight_lines': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 
                'placeholder': 'Ej: 1,3,5-7'
            }),
            'theme': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'height': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
                'min': '200',
                'max': '800',
                'step': '50',
                'value': '300'
            }),
            'is_editable': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
            'show_line_numbers': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
            'wrap_lines': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
            'allow_student_submissions': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-indigo-600 focus:ring-indigo-500 border-gray-300 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        step = kwargs.pop('step', None)
        super().__init__(*args, **kwargs)
        
        # Si se proporciona un paso, preestablecerlo y calcular el siguiente orden
        if step:
            self.fields['step'].initial = step
            if not self.instance.pk:  # Si es un objeto nuevo
                next_order = CodeBlock.objects.filter(step=step).count() + 1
                self.fields['order'].initial = next_order

    def clean_highlight_lines(self):
        """Validar el formato de líneas a resaltar"""
        highlight_lines = self.cleaned_data.get('highlight_lines')
        if not highlight_lines:
            return highlight_lines
            
        # Validar formato (1,3,5-7)
        parts = highlight_lines.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                try:
                    start, end = map(int, part.split('-'))
                    if start >= end:
                        raise ValidationError(_('En un rango, el inicio debe ser menor que el fin.'))
                except ValueError:
                    raise ValidationError(_('Formato incorrecto para rango de líneas. Use "inicio-fin".'))
            else:
                try:
                    int(part)
                except ValueError:
                    raise ValidationError(_('Las líneas deben ser números enteros.'))
                    
        return highlight_lines

    def clean(self):
        cleaned_data = super().clean()
        is_editable = cleaned_data.get('is_editable')
        allow_submissions = cleaned_data.get('allow_student_submissions')
        
        # Si permite envíos, debe ser editable
        if allow_submissions and not is_editable:
            raise ValidationError(_('Para permitir envíos de estudiantes, el código debe ser editable.'))
        
        return cleaned_data


class ExplanationBlockForm(forms.ModelForm):
    """Formulario para crear y editar Bloques de Explicación"""

    class Meta:
        model = ExplanationBlock
        fields = ['step', 'content', 'order', 'related_code_block']
        widgets = {
            'step': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 8}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'related_code_block': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
        }

    def __init__(self, *args, **kwargs):
        step = kwargs.pop('step', None)
        super().__init__(*args, **kwargs)
        
        # Si se proporciona un paso, preestablecerlo y calcular el siguiente orden
        if step:
            self.fields['step'].initial = step
            self.fields['related_code_block'].queryset = CodeBlock.objects.filter(step=step)
            
            if not self.instance.pk:  # Si es un objeto nuevo
                next_order = ExplanationBlock.objects.filter(step=step).count() + 1
                self.fields['order'].initial = next_order
        else:
            # Si no se proporciona un paso, filtrar el queryset basado en el paso seleccionado actualmente
            if self.instance and self.instance.step:
                self.fields['related_code_block'].queryset = CodeBlock.objects.filter(step=self.instance.step)
            else:
                self.fields['related_code_block'].queryset = CodeBlock.objects.none()


class QuestionBlockForm(forms.ModelForm):
    """Formulario para crear y editar Bloques de Pregunta"""

    class Meta:
        model = QuestionBlock
        fields = ['step', 'question_text', 'correct_answer', 'order', 'related_code_block']
        widgets = {
            'step': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'question_text': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 3}),
            'correct_answer': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'related_code_block': forms.Select(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
        }

    def __init__(self, *args, **kwargs):
        step = kwargs.pop('step', None)
        super().__init__(*args, **kwargs)
        
        # Si se proporciona un paso, preestablecerlo y filtrar bloques de código relacionados
        if step:
            self.fields['step'].initial = step
            self.fields['related_code_block'].queryset = CodeBlock.objects.filter(step=step)
            
            if not self.instance.pk:  # Si es un objeto nuevo
                next_order = QuestionBlock.objects.filter(step=step).count() + 1
                self.fields['order'].initial = next_order
        else:
            # Si no se proporciona un paso, filtrar el queryset basado en el paso seleccionado actualmente
            if self.instance and self.instance.step:
                self.fields['related_code_block'].queryset = CodeBlock.objects.filter(step=self.instance.step)
            else:
                self.fields['related_code_block'].queryset = CodeBlock.objects.none()


class StudentResponseForm(forms.ModelForm):
    """Formulario para registrar respuestas de estudiantes"""

    class Meta:
        model = StudentResponse
        fields = ['response_text']
        widgets = {
            'response_text': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500', 'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)


# NUEVO FORMULARIO para envíos de código de estudiantes
class StudentCodeSubmissionForm(forms.ModelForm):
    """Formulario para que los estudiantes envíen código"""

    class Meta:
        model = StudentCodeSubmission
        fields = ['submitted_code']
        widgets = {
            'submitted_code': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 font-mono',
                'rows': 10,
                'style': 'font-family: "Courier New", Courier, monospace;'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.code_block = kwargs.pop('code_block', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)