# Register your models here.
from django.contrib import admin
from .models import DailyProgress
from .models import ChatMessage
from .models import Complaint

admin.site.register(ChatMessage)

admin.site.register(DailyProgress)

admin.site.register(Complaint)