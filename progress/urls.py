from django.urls import path
from . import views
from django.urls import path
from .views import chat_select, teacher_chat, chat_room
from .views import submit_complaint

urlpatterns = [
    path('add-progress/', views.add_progress, name='add_progress'),
    path('chat-select/', chat_select, name='chat_select'),
    path('teacher-chat/', teacher_chat, name='teacher_chat'),
    path('chat/<int:user_id>/', chat_room, name='chat_room'),
    path('get-messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('complaint/', submit_complaint, name='submit_complaint'),
]


