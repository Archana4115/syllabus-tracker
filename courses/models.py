from django.db import models
from django.conf import settings

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    class_name = models.CharField(max_length=100)
    total_planned_lectures = models.IntegerField(default=0)

    def __str__(self):
        return self.course_name

    # ✅ FINAL FIXED FUNCTION
    def get_completion_percentage(self):
        total_topics = 0
        completed_topics = 0

        for unit in self.units.all():   # Course → Unit
            topics = unit.topics.all()    # Unit → Topic (related_name='topics')

            total_topics += topics.count()
            completed_topics += topics.filter(is_completed=True).count()

        if total_topics == 0:
            return 0
        
        return int((completed_topics / total_topics) * 100)

    # ✅ Behind Schedule
    def is_behind_schedule(self):
        return self.get_completion_percentage() < 50
    
class Unit(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    unit_name = models.CharField(max_length=200)
    planned_lectures = models.IntegerField(default=0)

    def __str__(self):
        return self.unit_name


class Topic(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name='topics')
    topic_name = models.CharField(max_length=200)
    planned_lectures = models.FloatField(default=0)
    planned_start_date = models.DateField()
    planned_end_date = models.DateField()

    # ✅ MUST ADD THIS
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.topic_name

class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.username} - {self.course.course_name}"
    
    def get_completion_percentage(self):
        return 0  # temporary fix (no error)
    