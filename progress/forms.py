from django import forms
from .models import DailyProgress
from django.contrib.auth.forms import AuthenticationForm

class DailyProgressForm(forms.ModelForm):
    class Meta:
        model = DailyProgress
        fields = '__all__'

class TeacherLoginForm(AuthenticationForm):
    pass

class StudentLoginForm(AuthenticationForm):
    pass