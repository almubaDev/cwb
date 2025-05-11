from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Module, Week, Session, VideoClass
from .forms import CourseForm, ModuleForm, WeekForm, SessionForm, VideoClassForm


# Añade esta función a views.py

def dashboard(request):
    # Contar objetos por modelo
    total_courses = Course.objects.count()
    total_modules = Module.objects.count()
    total_weeks = Week.objects.count()
    total_sessions = Session.objects.count()
    
    # Obtener cursos recientes
    recent_courses = Course.objects.all().order_by('-created')[:5]
    
    # Simular actividad reciente
    # En una aplicación real, podrías usar un modelo de Activity o similar
    recent_activities = []
    
    # Cursos recientes
    for course in Course.objects.all().order_by('-created')[:3]:
        recent_activities.append({
            'type': 'course',
            'message': f'Curso "{course.title}" creado',
            'time': course.created
        })
    
    # Módulos recientes
    for module in Module.objects.all().order_by('-created')[:3]:
        recent_activities.append({
            'type': 'module',
            'message': f'Módulo "{module.title}" añadido al curso "{module.course.title}"',
            'time': module.created
        })
    
    # Semanas recientes
    for week in Week.objects.all().order_by('-created')[:3]:
        recent_activities.append({
            'type': 'week',
            'message': f'Semana "{week.title}" añadida al módulo "{week.module.title}"',
            'time': week.created
        })
    
    # Sesiones recientes
    for session in Session.objects.all().order_by('-created')[:3]:
        recent_activities.append({
            'type': 'session',
            'message': f'Sesión "{session.title}" añadida a la semana "{session.week.title}"',
            'time': session.created
        })
    
    # Ordenar actividades por tiempo (más recientes primero)
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:10]  # Limitar a 10 actividades
    
    context = {
        'total_courses': total_courses,
        'total_modules': total_modules,
        'total_weeks': total_weeks,
        'total_sessions': total_sessions,
        'recent_courses': recent_courses,
        'recent_activities': recent_activities,
    }
    
    return render(request, 'courses/dashboard.html', context)



# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('courses:course_list')


class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    context_object_name = 'course'
    
    def get_success_url(self):
        return reverse_lazy('courses:course_detail', kwargs={'pk': self.object.pk})


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy('courses:course_list')


# Module Views
class ModuleListView(ListView):
    model = Module
    template_name = 'courses/module_list.html'
    context_object_name = 'modules'
    
    def get_queryset(self):
        if 'course_id' in self.kwargs:
            return Module.objects.filter(course_id=self.kwargs['course_id'])
        return Module.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'course_id' in self.kwargs:
            context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context


class ModuleDetailView(DetailView):
    model = Module
    template_name = 'courses/module_detail.html'
    context_object_name = 'module'


class ModuleCreateView(LoginRequiredMixin, CreateView):
    model = Module
    form_class = ModuleForm
    template_name = 'courses/module_form.html'
    
    def get_initial(self):
        if 'course_id' in self.kwargs:
            return {'course': self.kwargs['course_id']}
        return {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'course_id' in self.kwargs:
            context['course'] = get_object_or_404(Course, id=self.kwargs['course_id'])
        return context
    
    def get_success_url(self):
        if 'course_id' in self.kwargs:
            return reverse_lazy('courses:module_list', kwargs={'course_id': self.kwargs['course_id']})
        return reverse_lazy('courses:module_list')


class ModuleUpdateView(LoginRequiredMixin, UpdateView):
    model = Module
    form_class = ModuleForm
    template_name = 'courses/module_form.html'
    context_object_name = 'module'
    
    def get_success_url(self):
        return reverse_lazy('courses:module_detail', kwargs={'pk': self.object.pk})


class ModuleDeleteView(LoginRequiredMixin, DeleteView):
    model = Module
    template_name = 'courses/module_confirm_delete.html'
    context_object_name = 'module'
    
    def get_success_url(self):
        return reverse_lazy('courses:module_list', kwargs={'course_id': self.object.course.id})


# Week Views
class WeekListView(ListView):
    model = Week
    template_name = 'courses/week_list.html'
    context_object_name = 'weeks'
    
    def get_queryset(self):
        if 'module_id' in self.kwargs:
            return Week.objects.filter(module_id=self.kwargs['module_id'])
        return Week.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'module_id' in self.kwargs:
            context['module'] = get_object_or_404(Module, id=self.kwargs['module_id'])
        return context


class WeekDetailView(DetailView):
    model = Week
    template_name = 'courses/week_detail.html'
    context_object_name = 'week'


class WeekCreateView(LoginRequiredMixin, CreateView):
    model = Week
    form_class = WeekForm
    template_name = 'courses/week_form.html'
    
    def get_initial(self):
        if 'module_id' in self.kwargs:
            return {'module': self.kwargs['module_id']}
        return {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'module_id' in self.kwargs:
            context['module'] = get_object_or_404(Module, id=self.kwargs['module_id'])
        return context
    
    def get_success_url(self):
        if 'module_id' in self.kwargs:
            return reverse_lazy('courses:week_list', kwargs={'module_id': self.kwargs['module_id']})
        return reverse_lazy('courses:week_list')


class WeekUpdateView(LoginRequiredMixin, UpdateView):
    model = Week
    form_class = WeekForm
    template_name = 'courses/week_form.html'
    context_object_name = 'week'
    
    def get_success_url(self):
        return reverse_lazy('courses:week_detail', kwargs={'pk': self.object.pk})


class WeekDeleteView(LoginRequiredMixin, DeleteView):
    model = Week
    template_name = 'courses/week_confirm_delete.html'
    context_object_name = 'week'
    
    def get_success_url(self):
        return reverse_lazy('courses:week_list', kwargs={'module_id': self.object.module.id})


# Session Views
class SessionListView(ListView):
    model = Session
    template_name = 'courses/session_list.html'
    context_object_name = 'sessions'
    
    def get_queryset(self):
        if 'week_id' in self.kwargs:
            return Session.objects.filter(week_id=self.kwargs['week_id'])
        return Session.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'week_id' in self.kwargs:
            context['week'] = get_object_or_404(Week, id=self.kwargs['week_id'])
        return context


class SessionDetailView(DetailView):
    model = Session
    template_name = 'courses/session_detail.html'
    context_object_name = 'session'


class SessionCreateView(LoginRequiredMixin, CreateView):
    model = Session
    form_class = SessionForm
    template_name = 'courses/session_form.html'
    
    def get_initial(self):
        if 'week_id' in self.kwargs:
            return {'week': self.kwargs['week_id']}
        return {}
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'week_id' in self.kwargs:
            context['week'] = get_object_or_404(Week, id=self.kwargs['week_id'])
        return context
    
    def get_success_url(self):
        if 'week_id' in self.kwargs:
            return reverse_lazy('courses:session_list', kwargs={'week_id': self.kwargs['week_id']})
        return reverse_lazy('courses:session_list')


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    model = Session
    form_class = SessionForm
    template_name = 'courses/session_form.html'
    context_object_name = 'session'
    
    def get_success_url(self):
        return reverse_lazy('courses:session_detail', kwargs={'pk': self.object.pk})


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = Session
    template_name = 'courses/session_confirm_delete.html'
    context_object_name = 'session'
    
    def get_success_url(self):
        return reverse_lazy('courses:session_list', kwargs={'week_id': self.object.week.id})
    
    
# VideoClass Views
class VideoClassListView(ListView):
    model = VideoClass
    template_name = 'courses/videoclass_list.html'
    context_object_name = 'videos'
    
    def get_queryset(self):
        if 'session_id' in self.kwargs:
            return VideoClass.objects.filter(session_id=self.kwargs['session_id'])
        return VideoClass.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'session_id' in self.kwargs:
            context['session'] = get_object_or_404(Session, id=self.kwargs['session_id'])
        return context


class VideoClassDetailView(DetailView):
    model = VideoClass
    template_name = 'courses/videoclass_detail.html'
    context_object_name = 'video'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        video = self.get_object()
        context['embed_url'] = video.get_embed_url()
        context['platform'] = video.video_platform()
        
        # Obtener videos de la misma sesión para navegación
        context['session_videos'] = VideoClass.objects.filter(
            session=video.session
        ).order_by('order')
        
        # Obtener el siguiente y anterior video
        context['next_video'] = video.get_next_content()
        context['prev_video'] = video.get_previous_content()
        
        return context


class VideoClassCreateView(LoginRequiredMixin, CreateView):
    model = VideoClass
    form_class = VideoClassForm
    template_name = 'courses/videoclass_form.html'
    
    def get_initial(self):
        initial = {}
        if 'session_id' in self.kwargs:
            initial['session'] = self.kwargs['session_id']
            # Establecer el siguiente orden disponible
            session = get_object_or_404(Session, id=self.kwargs['session_id'])
            count = VideoClass.objects.filter(session=session).count()
            initial['order'] = count + 1
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'session_id' in self.kwargs:
            context['session'] = get_object_or_404(Session, id=self.kwargs['session_id'])
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        if 'session_id' in self.kwargs:
            return reverse_lazy('courses:videoclass_list', kwargs={'session_id': self.kwargs['session_id']})
        return reverse_lazy('courses:videoclass_list')


class VideoClassUpdateView(LoginRequiredMixin, UpdateView):
    model = VideoClass
    form_class = VideoClassForm
    template_name = 'courses/videoclass_form.html'
    context_object_name = 'video'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_update'] = True
        return context
    
    def get_success_url(self):
        return reverse_lazy('courses:videoclass_detail', kwargs={'pk': self.object.pk})


class VideoClassDeleteView(LoginRequiredMixin, DeleteView):
    model = VideoClass
    template_name = 'courses/videoclass_confirm_delete.html'
    context_object_name = 'video'
    
    def get_success_url(self):
        session_id = self.object.session.id
        return reverse_lazy('courses:videoclass_list', kwargs={'session_id': session_id})