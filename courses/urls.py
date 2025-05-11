from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Course URLs
    path('', views.dashboard, name='dashboard'),
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/', views.CourseDetailView.as_view(), name='course_detail'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # Module URLs - generales y específicas por curso
    path('modules/', views.ModuleListView.as_view(), name='module_list'),
    path('courses/<int:course_id>/modules/', views.ModuleListView.as_view(), name='module_list'),
    path('courses/<int:course_id>/modules/create/', views.ModuleCreateView.as_view(), name='module_create'),
    path('modules/<int:pk>/', views.ModuleDetailView.as_view(), name='module_detail'),
    path('modules/<int:pk>/update/', views.ModuleUpdateView.as_view(), name='module_update'),
    path('modules/<int:pk>/delete/', views.ModuleDeleteView.as_view(), name='module_delete'),
    
    # Week URLs - generales y específicas por módulo
    path('weeks/', views.WeekListView.as_view(), name='week_list'),
    path('modules/<int:module_id>/weeks/', views.WeekListView.as_view(), name='week_list'),
    path('modules/<int:module_id>/weeks/create/', views.WeekCreateView.as_view(), name='week_create'),
    path('weeks/<int:pk>/', views.WeekDetailView.as_view(), name='week_detail'),
    path('weeks/<int:pk>/update/', views.WeekUpdateView.as_view(), name='week_update'),
    path('weeks/<int:pk>/delete/', views.WeekDeleteView.as_view(), name='week_delete'),
    
    # Session URLs - generales y específicas por semana
    path('sessions/', views.SessionListView.as_view(), name='session_list'),
    path('weeks/<int:week_id>/sessions/', views.SessionListView.as_view(), name='session_list'),
    path('weeks/<int:week_id>/sessions/create/', views.SessionCreateView.as_view(), name='session_create'),
    path('sessions/<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
    path('sessions/<int:pk>/update/', views.SessionUpdateView.as_view(), name='session_update'),
    path('sessions/<int:pk>/delete/', views.SessionDeleteView.as_view(), name='session_delete'),
    
    # Video Class URLs - generales y específicas por sesión
    path('videos/', views.VideoClassListView.as_view(), name='videoclass_list'),
    path('sessions/<int:session_id>/videos/', views.VideoClassListView.as_view(), name='videoclass_list'),
    path('sessions/<int:session_id>/videos/create/', views.VideoClassCreateView.as_view(), name='videoclass_create'),
    path('videos/<int:pk>/', views.VideoClassDetailView.as_view(), name='videoclass_detail'),
    path('videos/<int:pk>/update/', views.VideoClassUpdateView.as_view(), name='videoclass_update'),
    path('videos/<int:pk>/delete/', views.VideoClassDeleteView.as_view(), name='videoclass_delete'),
]