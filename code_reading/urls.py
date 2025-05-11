# code_reading/urls.py
from django.urls import path
from . import views

app_name = 'code_reading'

urlpatterns = [
    # Vistas de CodeReading
    path('readings/', views.CodeReadingListView.as_view(), name='codereading_list'),
    path('sessions/<int:session_id>/readings/', views.CodeReadingListView.as_view(), name='codereading_list'),
    path('sessions/<int:session_id>/readings/create/', views.CodeReadingCreateView.as_view(), name='codereading_create'),
    path('readings/<int:pk>/', views.CodeReadingDetailView.as_view(), name='codereading_detail'),
    path('readings/<int:pk>/update/', views.CodeReadingUpdateView.as_view(), name='codereading_update'),
    path('readings/<int:pk>/delete/', views.CodeReadingDeleteView.as_view(), name='codereading_delete'),
    
    # Vistas de CodeReadingStep
    path('readings/<int:code_reading_id>/steps/create/', views.CodeReadingStepCreateView.as_view(), name='step_create'),
    path('steps/<int:pk>/', views.CodeReadingStepDetailView.as_view(), name='step_detail'),
    path('steps/<int:pk>/update/', views.CodeReadingStepUpdateView.as_view(), name='step_update'),
    path('steps/<int:pk>/delete/', views.CodeReadingStepDeleteView.as_view(), name='step_delete'),
    
    # Vistas de CodeBlock
    path('steps/<int:step_id>/codeblock/create/', views.CodeBlockCreateView.as_view(), name='codeblock_create'),
    path('codeblock/<int:pk>/update/', views.CodeBlockUpdateView.as_view(), name='codeblock_update'),
    path('codeblock/<int:pk>/delete/', views.CodeBlockDeleteView.as_view(), name='codeblock_delete'),
    
    # Vistas de ExplanationBlock
    path('steps/<int:step_id>/explanation/create/', views.ExplanationBlockCreateView.as_view(), name='explanation_create'),
    path('explanation/<int:pk>/update/', views.ExplanationBlockUpdateView.as_view(), name='explanation_update'),
    path('explanation/<int:pk>/delete/', views.ExplanationBlockDeleteView.as_view(), name='explanation_delete'),
    
    # Vistas de QuestionBlock
    path('steps/<int:step_id>/question/create/', views.QuestionBlockCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/update/', views.QuestionBlockUpdateView.as_view(), name='question_update'),
    path('question/<int:pk>/delete/', views.QuestionBlockDeleteView.as_view(), name='question_delete'),
    
    # Vistas para estudiantes
    path('student/readings/<int:pk>/', views.StudentCodeReadingView.as_view(), name='student_codereading'),
    path('student/readings/<int:pk>/steps/<int:step_id>/', views.StudentCodeReadingView.as_view(), name='student_step'),
    path('student/response/<int:question_id>/', views.SubmitStudentResponseView.as_view(), name='submit_response'),
    
    # Vistas complementarias
    path('sessions/<int:session_id>/code_readings/', views.session_code_readings, name='session_code_readings'),
    
    # *** ENDPOINTS API PARA AJAX ***
    # API para Steps
    path('api/steps/', views.step_api, name='api_steps'),
    path('api/steps/<int:step_id>/', views.step_detail_api, name='api_step_detail'),
    path('api/steps/<int:step_id>/code_blocks/', views.step_code_blocks_api, name='api_step_code_blocks'),
    
    # API para CodeBlocks
    path('api/code_blocks/', views.code_block_api, name='api_code_blocks'),
    path('api/code_blocks/<int:block_id>/', views.code_block_detail_api, name='api_code_block_detail'),
    
    # API para ExplanationBlocks
    path('api/explanation_blocks/', views.explanation_block_api, name='api_explanation_blocks'),
    path('api/explanation_blocks/<int:block_id>/', views.explanation_block_detail_api, name='api_explanation_block_detail'),
    
    # API para QuestionBlocks
    path('api/question_blocks/', views.question_block_api, name='api_question_blocks'),
    path('api/question_blocks/<int:block_id>/', views.question_block_detail_api, name='api_question_block_detail'),
]