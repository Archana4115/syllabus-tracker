from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_report, name='teacher_report'),
    path('student/', views.student_report, name='student_report'),
    path('download/', views.download_report, name='download_report'),
]