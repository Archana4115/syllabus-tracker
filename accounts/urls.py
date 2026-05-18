from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import user_login

urlpatterns = [
    # ✅ Login URLs
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('student/login/', views.student_login, name='student_login'),
    # ✅ Logout
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('login/', user_login, name='login'),
]