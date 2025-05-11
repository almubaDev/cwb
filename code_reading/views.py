# code_reading/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.db.models import Prefetch
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
import json

from .models import (
    CodeReading, CodeReadingStep, CodeBlock, 
    ExplanationBlock, QuestionBlock, StudentResponse, StudentProgress
)
from .forms import (
    CodeReadingForm, CodeReadingStepForm, CodeBlockForm, 
    ExplanationBlockForm, QuestionBlockForm, StudentResponseForm
)
from courses.models import Session

# ----- Vistas para CodeReading -----

class CodeReadingListView(ListView):
    model = CodeReading
    template_name = 'code_reading/codereading_list.html'
    context_object_name = 'code_readings'
    
    def get_queryset(self):
        if 'session_id' in self.kwargs:
            return CodeReading.objects.filter(session_id=self.kwargs['session_id'])
        return CodeReading.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'session_id' in self.kwargs:
            context['session'] = get_object_or_404(Session, id=self.kwargs['session_id'])
        return context


class CodeReadingDetailView(DetailView):
    model = CodeReading
    template_name = 'code_reading/codereading_detail.html'
    context_object_name = 'code_reading'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener pasos asociados con sus bloques
        steps = CodeReadingStep.objects.filter(code_reading=self.object).order_by('order')
        context['steps'] = steps
        
        # Información para crear nuevo paso
        context['next_step_order'] = steps.count() + 1 if steps else 1
        
        return context


class CodeReadingCreateView(LoginRequiredMixin, CreateView):
    model = CodeReading
    form_class = CodeReadingForm
    template_name = 'code_reading/codereading_form.html'
    
    def get_initial(self):
        initial = {}
        if 'session_id' in self.kwargs:
            initial['session'] = self.kwargs['session_id']
            # Establecer el siguiente orden disponible
            session = get_object_or_404(Session, id=self.kwargs['session_id'])
            count = CodeReading.objects.filter(session=session).count()
            initial['order'] = count + 1
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'session_id' in self.kwargs:
            context['session'] = get_object_or_404(Session, id=self.kwargs['session_id'])
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('code_reading:codereading_detail', kwargs={'pk': self.object.pk})


class CodeReadingUpdateView(LoginRequiredMixin, UpdateView):
    model = CodeReading
    form_class = CodeReadingForm
    template_name = 'code_reading/codereading_form.html'
    context_object_name = 'code_reading'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        
        # Obtener pasos asociados con sus bloques para mostrar en la vista
        steps = CodeReadingStep.objects.filter(code_reading=self.object).order_by('order')
        context['steps'] = steps
        
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def get_success_url(self):
        return reverse_lazy('code_reading:codereading_detail', kwargs={'pk': self.object.pk})


class CodeReadingDeleteView(LoginRequiredMixin, DeleteView):
    model = CodeReading
    template_name = 'code_reading/codereading_confirm_delete.html'
    context_object_name = 'code_reading'
    
    def get_success_url(self):
        session_id = self.object.session.id
        return reverse_lazy('code_reading:codereading_list', kwargs={'session_id': session_id})


# ----- Vistas para CodeReadingStep -----

class CodeReadingStepCreateView(LoginRequiredMixin, CreateView):
    model = CodeReadingStep
    form_class = CodeReadingStepForm
    template_name = 'code_reading/step_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'code_reading_id' in self.kwargs:
            kwargs['code_reading'] = get_object_or_404(CodeReading, id=self.kwargs['code_reading_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'code_reading_id' in self.kwargs:
            context['code_reading'] = get_object_or_404(CodeReading, id=self.kwargs['code_reading_id'])
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:codereading_detail', kwargs={'pk': self.object.code_reading.pk})


class CodeReadingStepUpdateView(LoginRequiredMixin, UpdateView):
    model = CodeReadingStep
    form_class = CodeReadingStepForm
    template_name = 'code_reading/step_form.html'
    context_object_name = 'step'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['code_reading'] = self.object.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:codereading_detail', kwargs={'pk': self.object.code_reading.pk})


class CodeReadingStepDeleteView(LoginRequiredMixin, DeleteView):
    model = CodeReadingStep
    template_name = 'code_reading/step_confirm_delete.html'
    context_object_name = 'step'
    
    def get_success_url(self):
        return reverse_lazy('code_reading:codereading_detail', kwargs={'pk': self.object.code_reading.pk})


class CodeReadingStepDetailView(DetailView):
    model = CodeReadingStep
    template_name = 'code_reading/step_detail.html'
    context_object_name = 'step'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener bloques de código, explicaciones y preguntas ordenados
        context['code_blocks'] = CodeBlock.objects.filter(step=self.object).order_by('order')
        context['explanation_blocks'] = ExplanationBlock.objects.filter(step=self.object).order_by('order')
        context['question_blocks'] = QuestionBlock.objects.filter(step=self.object).order_by('order')
        
        # Información para nuevos elementos
        context['next_code_order'] = context['code_blocks'].count() + 1 if context['code_blocks'] else 1
        context['next_explanation_order'] = context['explanation_blocks'].count() + 1 if context['explanation_blocks'] else 1
        context['next_question_order'] = context['question_blocks'].count() + 1 if context['question_blocks'] else 1
        
        return context


# ----- Vistas para CodeBlock -----

class CodeBlockCreateView(LoginRequiredMixin, CreateView):
    model = CodeBlock
    form_class = CodeBlockForm
    template_name = 'code_reading/codeblock_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'step_id' in self.kwargs:
            kwargs['step'] = get_object_or_404(CodeReadingStep, id=self.kwargs['step_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'step_id' in self.kwargs:
            step = get_object_or_404(CodeReadingStep, id=self.kwargs['step_id'])
            context['step'] = step
            context['code_reading'] = step.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


class CodeBlockUpdateView(LoginRequiredMixin, UpdateView):
    model = CodeBlock
    form_class = CodeBlockForm
    template_name = 'code_reading/codeblock_form.html'
    context_object_name = 'code_block'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['step'] = self.object.step
        context['code_reading'] = self.object.step.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


class CodeBlockDeleteView(LoginRequiredMixin, DeleteView):
    model = CodeBlock
    template_name = 'code_reading/codeblock_confirm_delete.html'
    context_object_name = 'code_block'
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


# ----- Vistas para ExplanationBlock -----

class ExplanationBlockCreateView(LoginRequiredMixin, CreateView):
    model = ExplanationBlock
    form_class = ExplanationBlockForm
    template_name = 'code_reading/explanation_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'step_id' in self.kwargs:
            kwargs['step'] = get_object_or_404(CodeReadingStep, id=self.kwargs['step_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'step_id' in self.kwargs:
            step = get_object_or_404(CodeReadingStep, id=self.kwargs['step_id'])
            context['step'] = step
            context['code_reading'] = step.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


class ExplanationBlockUpdateView(LoginRequiredMixin, UpdateView):
    model = ExplanationBlock
    form_class = ExplanationBlockForm
    template_name = 'code_reading/explanation_form.html'
    context_object_name = 'explanation'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['step'] = self.object.step
        context['code_reading'] = self.object.step.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


class ExplanationBlockDeleteView(LoginRequiredMixin, DeleteView):
    model = ExplanationBlock
    template_name = 'code_reading/explanation_confirm_delete.html'
    context_object_name = 'explanation'
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


# ----- Vistas para QuestionBlock -----

class QuestionBlockCreateView(LoginRequiredMixin, CreateView):
    model = QuestionBlock
    form_class = QuestionBlockForm
    template_name = 'code_reading/question_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'step_id' in self.kwargs:
            kwargs['step'] = get_object_or_404(CodeReadingStep, id=self.kwargs['step_id'])
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'step_id' in self.kwargs:
            step = get_object_or_404(CodeReadingStep, id=self.kwargs['step_id'])
            context['step'] = step
            context['code_reading'] = step.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


class QuestionBlockUpdateView(LoginRequiredMixin, UpdateView):
    model = QuestionBlock
    form_class = QuestionBlockForm
    template_name = 'code_reading/question_form.html'
    context_object_name = 'question'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        context['step'] = self.object.step
        context['code_reading'] = self.object.step.code_reading
        return context
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


class QuestionBlockDeleteView(LoginRequiredMixin, DeleteView):
    model = QuestionBlock
    template_name = 'code_reading/question_confirm_delete.html'
    context_object_name = 'question'
    
    def get_success_url(self):
        return reverse_lazy('code_reading:step_detail', kwargs={'pk': self.object.step.pk})


# ----- Vistas para Estudiantes -----

class StudentCodeReadingView(LoginRequiredMixin, DetailView):
    """Vista principal para que los estudiantes realicen la lectura de código"""
    model = CodeReading
    template_name = 'code_reading/student/codereading_view.html'
    context_object_name = 'code_reading'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Obtener o crear el registro de progreso del estudiante
        progress, created = StudentProgress.objects.get_or_create(
            user=user,
            code_reading=self.object,
            defaults={'current_step': None}
        )
        
        # Determinar el paso actual
        if 'step_id' in self.kwargs:
            current_step = get_object_or_404(
                CodeReadingStep, 
                id=self.kwargs['step_id'],
                code_reading=self.object
            )
        elif progress.current_step:
            current_step = progress.current_step
        else:
            # Obtener el primer paso si no hay uno actual
            current_step = CodeReadingStep.objects.filter(
                code_reading=self.object
            ).order_by('order').first()
        
        if current_step:
            # Actualizar el paso actual en el progreso
            if progress.current_step != current_step:
                progress.current_step = current_step
                progress.save()
            
            # Obtener los bloques de código, explicaciones y preguntas para el paso actual
            code_blocks = CodeBlock.objects.filter(step=current_step).order_by('order')
            explanation_blocks = ExplanationBlock.objects.filter(step=current_step).order_by('order')
            questions = QuestionBlock.objects.filter(step=current_step).order_by('order')
            
            # Obtener respuestas existentes del estudiante
            student_responses = {
                sr.question_id: sr
                for sr in StudentResponse.objects.filter(
                    user=user,
                    question__step=current_step
                )
            }
            
            # Crear formularios para las preguntas sin respuesta
            question_forms = []
            for question in questions:
                if question.id in student_responses:
                    # Ya tiene respuesta
                    response = student_responses[question.id]
                    question_forms.append({
                        'question': question,
                        'form': None,
                        'response': response
                    })
                else:
                    # Sin respuesta aún
                    form = StudentResponseForm(question=question)
                    question_forms.append({
                        'question': question,
                        'form': form,
                        'response': None
                    })
            
            # Verificar si todas las preguntas obligatorias tienen respuesta
            all_answered = all(question.id in student_responses for question in questions)
            
            # Obtener pasos anterior y siguiente para navegación
            all_steps = list(CodeReadingStep.objects.filter(
                code_reading=self.object
            ).order_by('order'))
            
            current_index = all_steps.index(current_step)
            prev_step = all_steps[current_index - 1] if current_index > 0 else None
            next_step = all_steps[current_index + 1] if current_index < len(all_steps) - 1 else None
            
            # Añadir información al contexto
            context.update({
                'current_step': current_step,
                'code_blocks': code_blocks,
                'explanation_blocks': explanation_blocks,
                'question_forms': question_forms,
                'all_answered': all_answered,
                'progress': progress,
                'prev_step': prev_step,
                'next_step': next_step,
                'all_steps': all_steps,
                'current_index': current_index,
                'total_steps': len(all_steps)
            })
        
        return context


class SubmitStudentResponseView(LoginRequiredMixin, FormView):
    """Vista para enviar respuestas a preguntas"""
    form_class = StudentResponseForm
    http_method_names = ['post']
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        question_id = self.kwargs.get('question_id')
        kwargs['question'] = get_object_or_404(QuestionBlock, id=question_id)
        return kwargs
    
    def form_valid(self, form):
        question = get_object_or_404(QuestionBlock, id=self.kwargs.get('question_id'))
        
        # Crear o actualizar respuesta
        response, created = StudentResponse.objects.update_or_create(
            user=self.request.user,
            question=question,
            defaults={
                'response_text': form.cleaned_data['response_text'],
                'ai_feedback': ''  # Se actualizará con feedback de IA
            }
        )
        
        # Aquí iría la lógica para evaluar la respuesta con IA
        # Esta es una implementación básica que posteriormente se conectará con IA
        feedback = "Tu respuesta será evaluada por IA pronto."
        
        # Actualizar feedback
        response.ai_feedback = feedback
        response.save()
        
        # Actualizar progreso y marcar paso como completado si es necesario
        step = question.step
        progress = StudentProgress.objects.get(
            user=self.request.user,
            code_reading=step.code_reading
        )
        
        # Verificar si todas las preguntas del paso tienen respuesta
        all_questions = QuestionBlock.objects.filter(step=step)
        answered_questions = StudentResponse.objects.filter(
            user=self.request.user,
            question__step=step
        ).count()
        
        if answered_questions == all_questions.count():
            # Todas las preguntas tienen respuesta, marcar paso como completado
            progress.completed_steps.add(step)
            
            # Verificar si todos los pasos están completados
            all_steps = CodeReadingStep.objects.filter(code_reading=step.code_reading)
            if progress.completed_steps.count() == all_steps.count():
                progress.is_completed = True
                progress.completed_at = timezone.now()
                messages.success(self.request, "¡Has completado esta lectura de código!")
            
            progress.save()
        
        # Retornar respuesta JSON con el resultado
        return JsonResponse({
            'success': True,
            'feedback': feedback
        })
    
    def form_invalid(self, form):
        return JsonResponse({
            'success': False,
            'errors': form.errors
        }, status=400)


# Vista para modificar session_detail.html
def session_code_readings(request, session_id):
    """Vista parcial para listar lecturas de código en la página de detalle de sesión"""
    session = get_object_or_404(Session, id=session_id)
    code_readings = CodeReading.objects.filter(session=session).order_by('order')
    
    return render(request, 'code_reading/partials/session_code_readings.html', {
        'session': session,
        'code_readings': code_readings
    })

# ----- NUEVAS VISTAS API PARA AJAX -----

@login_required
@require_http_methods(["GET", "POST"])
def step_api(request):
    """API para manejar pasos (crear)"""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code_reading = get_object_or_404(CodeReading, id=data.get('code_reading'))
            
            step = CodeReadingStep.objects.create(
                code_reading=code_reading,
                title=data.get('title'),
                order=data.get('order'),
                description=data.get('description', '')
            )
            
            return JsonResponse({
                'success': True,
                'step': {
                    'id': step.id,
                    'code_reading': step.code_reading.id,
                    'title': step.title,
                    'order': step.order,
                    'description': step.description
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'error': 'Método no permitido'
    }, status=405)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def step_detail_api(request, step_id):
    """API para manejar pasos (leer, actualizar, eliminar)"""
    step = get_object_or_404(CodeReadingStep, id=step_id)
    
    if request.method == "GET":
        return JsonResponse({
            'success': True,
            'step': {
                'id': step.id,
                'code_reading': step.code_reading.id,
                'title': step.title,
                'order': step.order,
                'description': step.description
            }
        })
    
    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            
            # Actualizar datos
            step.title = data.get('title', step.title)
            step.order = data.get('order', step.order)
            step.description = data.get('description', step.description)
            step.save()
            
            return JsonResponse({
                'success': True,
                'step': {
                    'id': step.id,
                    'code_reading': step.code_reading.id,
                    'title': step.title,
                    'order': step.order,
                    'description': step.description
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == "DELETE":
        try:
            step.delete()
            return JsonResponse({
                'success': True
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)


def step_code_blocks_api(request, step_id):
   """API para obtener los bloques de código de un paso"""
   step = get_object_or_404(CodeReadingStep, id=step_id)
   code_blocks = CodeBlock.objects.filter(step=step).order_by('order')
   
   blocks_data = []
   for block in code_blocks:
       # Limitar el código a los primeros 200 caracteres para la vista previa
       code_preview = block.code[:200] + ('...' if len(block.code) > 200 else '')
       
       blocks_data.append({
           'id': block.id,
           'step': block.step.id,
           'language': block.language,
           'order': block.order,
           'code': code_preview  # Solo para preview en selects
       })
   
   return JsonResponse({
       'success': True,
       'code_blocks': blocks_data
   })


@login_required
@require_http_methods(["GET", "POST"])
def code_block_api(request):
   """API para manejar bloques de código (crear)"""
   if request.method == "POST":
       try:
           data = json.loads(request.body)
           step = get_object_or_404(CodeReadingStep, id=data.get('step'))
           
           code_block = CodeBlock.objects.create(
               step=step,
               code=data.get('code'),
               language=data.get('language'),
               order=data.get('order'),
               highlight_lines=data.get('highlight_lines', '')
           )
           
           return JsonResponse({
               'success': True,
               'code_block': {
                   'id': code_block.id,
                   'step': code_block.step.id,
                   'language': code_block.language,
                   'order': code_block.order,
                   'code': code_block.code,
                   'highlight_lines': code_block.highlight_lines
               }
           })
           
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)
   
   return JsonResponse({
       'success': False,
       'error': 'Método no permitido'
   }, status=405)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def code_block_detail_api(request, block_id):
   """API para manejar bloques de código (leer, actualizar, eliminar)"""
   code_block = get_object_or_404(CodeBlock, id=block_id)
   
   if request.method == "GET":
       return JsonResponse({
           'success': True,
           'code_block': {
               'id': code_block.id,
               'step': code_block.step.id,
               'language': code_block.language,
               'order': code_block.order,
               'code': code_block.code,
               'highlight_lines': code_block.highlight_lines
           }
       })
   
   elif request.method == "PUT":
       try:
           data = json.loads(request.body)
           
           # Actualizar datos
           code_block.language = data.get('language', code_block.language)
           code_block.order = data.get('order', code_block.order)
           code_block.code = data.get('code', code_block.code)
           code_block.highlight_lines = data.get('highlight_lines', code_block.highlight_lines)
           code_block.save()
           
           return JsonResponse({
               'success': True,
               'code_block': {
                   'id': code_block.id,
                   'step': code_block.step.id,
                   'language': code_block.language,
                   'order': code_block.order,
                   'code': code_block.code,
                   'highlight_lines': code_block.highlight_lines
               }
           })
           
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)
   
   elif request.method == "DELETE":
       try:
           code_block.delete()
           return JsonResponse({
               'success': True
           })
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)


@login_required
@require_http_methods(["GET", "POST"])
def explanation_block_api(request):
   """API para manejar bloques de explicación (crear)"""
   if request.method == "POST":
       try:
           data = json.loads(request.body)
           step = get_object_or_404(CodeReadingStep, id=data.get('step'))
           
           # Manejar el bloque de código relacionado (opcional)
           related_code_block = None
           if data.get('related_code_block'):
               related_code_block = get_object_or_404(CodeBlock, id=data.get('related_code_block'))
           
           explanation = ExplanationBlock.objects.create(
               step=step,
               content=data.get('content'),
               order=data.get('order'),
               related_code_block=related_code_block
           )
           
           return JsonResponse({
               'success': True,
               'explanation_block': {
                   'id': explanation.id,
                   'step': explanation.step.id,
                   'content': explanation.content,
                   'order': explanation.order,
                   'related_code_block': explanation.related_code_block.id if explanation.related_code_block else None
               }
           })
           
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)
   
   return JsonResponse({
       'success': False,
       'error': 'Método no permitido'
   }, status=405)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def explanation_block_detail_api(request, block_id):
   """API para manejar bloques de explicación (leer, actualizar, eliminar)"""
   explanation = get_object_or_404(ExplanationBlock, id=block_id)
   
   if request.method == "GET":
       return JsonResponse({
           'success': True,
           'explanation_block': {
               'id': explanation.id,
               'step': explanation.step.id,
               'content': explanation.content,
               'order': explanation.order,
               'related_code_block': explanation.related_code_block.id if explanation.related_code_block else None
           }
       })
   
   elif request.method == "PUT":
       try:
           data = json.loads(request.body)
           
           # Manejar el bloque de código relacionado (opcional)
           related_code_block = None
           if data.get('related_code_block'):
               related_code_block = get_object_or_404(CodeBlock, id=data.get('related_code_block'))
           
           # Actualizar datos
           explanation.order = data.get('order', explanation.order)
           explanation.content = data.get('content', explanation.content)
           explanation.related_code_block = related_code_block
           explanation.save()
           
           return JsonResponse({
               'success': True,
               'explanation_block': {
                   'id': explanation.id,
                   'step': explanation.step.id,
                   'content': explanation.content,
                   'order': explanation.order,
                   'related_code_block': explanation.related_code_block.id if explanation.related_code_block else None
               }
           })
           
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)
   
   elif request.method == "DELETE":
       try:
           explanation.delete()
           return JsonResponse({
               'success': True
           })
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)


@login_required
@require_http_methods(["GET", "POST"])
def question_block_api(request):
   """API para manejar bloques de pregunta (crear)"""
   if request.method == "POST":
       try:
           data = json.loads(request.body)
           step = get_object_or_404(CodeReadingStep, id=data.get('step'))
           
           # Manejar el bloque de código relacionado (opcional)
           related_code_block = None
           if data.get('related_code_block'):
               related_code_block = get_object_or_404(CodeBlock, id=data.get('related_code_block'))
           
           question = QuestionBlock.objects.create(
               step=step,
               question_text=data.get('question_text'),
               correct_answer=data.get('correct_answer'),
               order=data.get('order'),
               related_code_block=related_code_block
           )
           
           return JsonResponse({
               'success': True,
               'question_block': {
                   'id': question.id,
                   'step': question.step.id,
                   'question_text': question.question_text,
                   'correct_answer': question.correct_answer,
                   'order': question.order,
                   'related_code_block': question.related_code_block.id if question.related_code_block else None
               }
           })
           
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)
   
   return JsonResponse({
       'success': False,
       'error': 'Método no permitido'
   }, status=405)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def question_block_detail_api(request, block_id):
   """API para manejar bloques de pregunta (leer, actualizar, eliminar)"""
   question = get_object_or_404(QuestionBlock, id=block_id)
   
   if request.method == "GET":
       return JsonResponse({
           'success': True,
           'question_block': {
               'id': question.id,
               'step': question.step.id,
               'question_text': question.question_text,
               'correct_answer': question.correct_answer,
               'order': question.order,
               'related_code_block': question.related_code_block.id if question.related_code_block else None
           }
       })
   
   elif request.method == "PUT":
       try:
           data = json.loads(request.body)
           
           # Manejar el bloque de código relacionado (opcional)
           related_code_block = None
           if data.get('related_code_block'):
               related_code_block = get_object_or_404(CodeBlock, id=data.get('related_code_block'))
           
           # Actualizar datos
           question.question_text = data.get('question_text', question.question_text)
           question.correct_answer = data.get('correct_answer', question.correct_answer)
           question.order = data.get('order', question.order)
           question.related_code_block = related_code_block
           question.save()
           
           return JsonResponse({
               'success': True,
               'question_block': {
                   'id': question.id,
                   'step': question.step.id,
                   'question_text': question.question_text,
                   'correct_answer': question.correct_answer,
                   'order': question.order,
                   'related_code_block': question.related_code_block.id if question.related_code_block else None
               }
           })
           
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)
   
   elif request.method == "DELETE":
       try:
           question.delete()
           return JsonResponse({
               'success': True
           })
       except Exception as e:
           return JsonResponse({
               'success': False,
               'error': str(e)
           }, status=400)