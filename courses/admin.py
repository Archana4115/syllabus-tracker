from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, Unit, Topic, Enrollment

admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Topic)
admin.site.register(Enrollment)