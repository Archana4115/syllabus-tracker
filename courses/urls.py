from . import views
from django.urls import path
from .views import teacher_dashboard, student_dashboard
from django.http import HttpResponse

urlpatterns = [
    path('', views.home, name='home'),  # homepage

    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
]

