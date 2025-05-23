# Generated by Django 5.2.1 on 2025-05-22 00:29

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('courses', '0002_videoclass'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CodeReading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metadata', models.JSONField(blank=True, default=dict, verbose_name='Metadatos adicionales')),
                ('duration_minutes', models.PositiveIntegerField(default=0, help_text='Tiempo estimado para completar este contenido', verbose_name='Duración estimada (minutos)')),
                ('available_from', models.DateTimeField(blank=True, help_text='Fecha a partir de la cual este contenido estará disponible', null=True, verbose_name='Disponible desde')),
                ('available_until', models.DateTimeField(blank=True, help_text='Fecha hasta la cual este contenido estará disponible', null=True, verbose_name='Disponible hasta')),
                ('tags', models.CharField(blank=True, help_text='Etiquetas separadas por comas para categorizar el contenido', max_length=255, verbose_name='Etiquetas')),
                ('difficulty_level', models.CharField(choices=[('beginner', 'Principiante'), ('intermediate', 'Intermedio'), ('advanced', 'Avanzado')], default='beginner', max_length=20, verbose_name='Nivel de dificultad')),
                ('title', models.CharField(max_length=255, verbose_name='Título')),
                ('description', models.TextField(blank=True, verbose_name='Descripción')),
                ('programming_language', models.CharField(choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('java', 'Java'), ('csharp', 'C#'), ('cpp', 'C++'), ('php', 'PHP'), ('ruby', 'Ruby'), ('go', 'Go'), ('swift', 'Swift'), ('typescript', 'TypeScript'), ('html', 'HTML'), ('css', 'CSS'), ('sql', 'SQL'), ('bash', 'Bash/Shell'), ('other', 'Otro')], default='python', help_text='Lenguaje de programación principal del código', max_length=50, verbose_name='Lenguaje de Programación')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Visible para estudiantes')),
                ('is_mandatory', models.BooleanField(default=False, verbose_name='Es obligatorio')),
                ('is_evaluable', models.BooleanField(default=False, verbose_name='Es evaluable')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_code_readings', to=settings.AUTH_USER_MODEL, verbose_name='Creado por')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_readings', to='courses.session', verbose_name='Sesión')),
            ],
            options={
                'verbose_name': 'Lectura de Código',
                'verbose_name_plural': 'Lecturas de Código',
                'ordering': ['session', 'order'],
            },
        ),
        migrations.CreateModel(
            name='CodeReadingStep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Título del paso')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('description', models.TextField(blank=True, verbose_name='Descripción general del paso')),
                ('code_reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='steps', to='code_reading.codereading', verbose_name='Lectura de Código')),
            ],
            options={
                'verbose_name': 'Paso de Lectura',
                'verbose_name_plural': 'Pasos de Lectura',
                'ordering': ['code_reading', 'order'],
            },
        ),
        migrations.CreateModel(
            name='CodeBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(verbose_name='Código')),
                ('language', models.CharField(choices=[('python', 'Python'), ('javascript', 'JavaScript'), ('html', 'HTML'), ('css', 'CSS'), ('sql', 'SQL'), ('bash', 'Bash/Shell'), ('json', 'JSON'), ('xml', 'XML'), ('yaml', 'YAML'), ('markdown', 'Markdown'), ('django-template', 'Django Template'), ('text', 'Texto plano')], default='python', max_length=50, verbose_name='Lenguaje')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('highlight_lines', models.CharField(blank=True, help_text="Formato: '1,3,5-7' para resaltar líneas 1, 3, y del 5 al 7", max_length=255, verbose_name='Líneas a resaltar')),
                ('is_editable', models.BooleanField(default=False, help_text='Si está marcado, los estudiantes podrán editar el código', verbose_name='¿Es editable?')),
                ('show_line_numbers', models.BooleanField(default=True, verbose_name='Mostrar números de línea')),
                ('theme', models.CharField(choices=[('vs', 'Visual Studio Light'), ('vs-dark', 'Visual Studio Dark'), ('hc-black', 'High Contrast Black'), ('monokai', 'Monokai'), ('github', 'GitHub'), ('solarized-dark', 'Solarized Dark'), ('solarized-light', 'Solarized Light')], default='vs-dark', max_length=20, verbose_name='Tema del editor')),
                ('height', models.PositiveIntegerField(default=300, help_text='Altura en píxeles del editor de código', verbose_name='Altura del editor (px)')),
                ('wrap_lines', models.BooleanField(default=False, verbose_name='Ajustar líneas largas')),
                ('allow_student_submissions', models.BooleanField(default=False, help_text="Si está marcado junto con 'es editable', los estudiantes podrán enviar su código", verbose_name='Permitir envío de soluciones')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_blocks', to='code_reading.codereadingstep', verbose_name='Paso')),
            ],
            options={
                'verbose_name': 'Bloque de Código',
                'verbose_name_plural': 'Bloques de Código',
                'ordering': ['step', 'order'],
            },
        ),
        migrations.CreateModel(
            name='ExplanationBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='Contenido de la explicación')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('related_code_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='explanations', to='code_reading.codeblock', verbose_name='Bloque de código relacionado')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='explanation_blocks', to='code_reading.codereadingstep', verbose_name='Paso')),
            ],
            options={
                'verbose_name': 'Bloque de Explicación',
                'verbose_name_plural': 'Bloques de Explicación',
                'ordering': ['step', 'order'],
            },
        ),
        migrations.CreateModel(
            name='QuestionBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.TextField(verbose_name='Texto de la pregunta')),
                ('correct_answer', models.TextField(help_text='Para IA: criterios de la respuesta correcta', verbose_name='Respuesta correcta')),
                ('order', models.PositiveIntegerField(default=1, verbose_name='Orden')),
                ('related_code_block', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='questions', to='code_reading.codeblock', verbose_name='Bloque de código relacionado')),
                ('step', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_blocks', to='code_reading.codereadingstep', verbose_name='Paso')),
            ],
            options={
                'verbose_name': 'Bloque de Pregunta',
                'verbose_name_plural': 'Bloques de Pregunta',
                'ordering': ['step', 'order'],
            },
        ),
        migrations.CreateModel(
            name='StudentCodeSubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_code', models.TextField(verbose_name='Código enviado por el estudiante')),
                ('is_final_submission', models.BooleanField(default=False, help_text='Marca la última versión enviada por el estudiante', verbose_name='¿Es envío final?')),
                ('ai_feedback', models.TextField(blank=True, verbose_name='Feedback de la IA')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('code_block', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_submissions', to='code_reading.codeblock', verbose_name='Bloque de código')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_submissions', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Envío de Código de Estudiante',
                'verbose_name_plural': 'Envíos de Código de Estudiantes',
                'ordering': ['-created'],
                'unique_together': {('user', 'code_block')},
            },
        ),
        migrations.CreateModel(
            name='StudentProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, verbose_name='¿Completado?')),
                ('started_at', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de inicio')),
                ('completed_at', models.DateTimeField(blank=True, null=True, verbose_name='Fecha de finalización')),
                ('code_reading', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_progress', to='code_reading.codereading', verbose_name='Lectura de Código')),
                ('completed_steps', models.ManyToManyField(blank=True, related_name='student_completed', to='code_reading.codereadingstep', verbose_name='Pasos completados')),
                ('current_step', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student_current', to='code_reading.codereadingstep', verbose_name='Paso actual')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_reading_progress', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Progreso de Estudiante',
                'verbose_name_plural': 'Progresos de Estudiantes',
                'unique_together': {('user', 'code_reading')},
            },
        ),
        migrations.CreateModel(
            name='StudentResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_text', models.TextField(verbose_name='Respuesta del estudiante')),
                ('ai_feedback', models.TextField(blank=True, verbose_name='Feedback de la IA')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Última actualización')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_responses', to='code_reading.questionblock', verbose_name='Pregunta')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='code_reading_responses', to=settings.AUTH_USER_MODEL, verbose_name='Estudiante')),
            ],
            options={
                'verbose_name': 'Respuesta de Estudiante',
                'verbose_name_plural': 'Respuestas de Estudiantes',
                'unique_together': {('user', 'question')},
            },
        ),
    ]
