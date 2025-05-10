# Crea un archivo llamado context_processors.py en la carpeta de la app courses

from .models import Course, Module, Week, Session

def courses_context(request):
    """
    Proporciona datos de contexto para todas las plantillas
    """
    return {
        'total_courses': Course.objects.count(),
        'total_modules': Module.objects.count(),
        'total_weeks': Week.objects.count(),
        'total_sessions': Session.objects.count(),
    }