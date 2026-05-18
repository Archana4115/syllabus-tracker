from django.urls import path
from . import views

urlpatterns = [
    path('teacher/', views.teacher_report, name='teacher_report'),
    path('student/', views.student_report, name='student_report'),
    path('download-pdf/', views.download_pdf_report, name='download_pdf'),
]