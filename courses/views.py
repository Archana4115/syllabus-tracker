# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Course
from datetime import date
from .models import Topic
from .models import Enrollment
from datetime import date, timedelta
from .models import Topic
from progress.models import Topic
from progress.models import ChatMessage
from progress.models import DailyProgress
from .models import Enrollment, Topic
from django.contrib.auth import get_user_model
User = get_user_model()


def home(request):
    return render(request, 'home.html')

from django.contrib.auth.decorators import login_required

@login_required
def teacher_dashboard(request):
    courses = Course.objects.filter(teacher=request.user)

    total = 0
    count = 0 

    course_names = []
    completion_data = []
    course_data = [] 

    for course in courses:
        completion = course.get_completion_percentage()

        course_data.append({
            'name': course.course_name,
            'completion': completion,
            'behind': course.is_behind_schedule()
        })

        course_names.append(course.course_name)
        completion_data.append(completion)

        total += completion
        count += 1

    overall_progress = round(total / count, 2) if count > 0 else 0

    print("Teacher Overall:", overall_progress)

    today = date.today()
    next_week = today + timedelta(days=7)

    upcoming_topics = Topic.objects.filter(
        planned_start_date__range=[today, next_week]
    )


    context = {
        'courses': course_data,
        'course_names': course_names,
        'completion_data': completion_data,
        'upcoming_topics': upcoming_topics,
        'overall_progress': overall_progress
    }

    completed_topics = Topic.objects.filter(
    completed=True
    ).count()

    pending_topics = Topic.objects.filter(
    completed=False
    ).count()

    return render(request, 'teacher_dashboard.html', {

    'courses': courses,
    'overall_progress': overall_progress,

    # PIE CHART DATA
    'completed_topics': completed_topics,
    'pending_topics': pending_topics,

})

@login_required
def student_dashboard(request):

    enrollments = Enrollment.objects.filter(student=request.user)

    course_data = []
    course_names = []
    completion_data = []
    progress_data = []
    overall_progress = []

    for enroll in enrollments:
        course = enroll.course
        completion = course.get_completion_percentage()

        course_data.append({
            'name': course.course_name,
            'completion': completion
        })

        course_names.append(course.course_name)
        completion_data.append(completion)

    total = 0 
    count = 0

    for enroll in enrollments:
        course = enroll.course
        completion = course.get_completion_percentage()
    
        total += completion
        count += 1

    if count > 0:
        overall_progress = round(total / count, 2)
    else:
        overall_progress = 0

    #  Upcoming topics (next 7 days)
    from datetime import timedelta
    today = date.today()
    next_week = today + timedelta(days=7)

    course_ids = [enroll.course.id for enroll in enrollments]

    upcoming_topics = Topic.objects.filter(
        unit__course__id__in=course_ids,
        planned_start_date__range=[today, next_week]
    )

        #missed topics
    missed_topics = Topic.objects.filter(
        unit__course__id__in=course_ids,
        planned_end_date__lt=today
    )

    progress_data = DailyProgress.objects.filter(
        topic__unit__course__in=[enroll.course for enroll in enrollments]
    ).order_by('-date')
    

    context = {
        'courses': course_data,
        'course_names': course_names,
        'completion_data': completion_data,
        'upcoming_topics': upcoming_topics,
        'missed_topics': missed_topics,
        'progress_data': progress_data,
        'overall_progress': overall_progress
    }

    return render(request, 'student_dashboard.html', context)

def add_progress(request):

    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        date = request.POST.get('date')
        lectures = request.POST.get('lectures')
        notes = request.POST.get('notes')
        attachment = request.FILES.get('attachment')

        topic = Topic.objects.get(id=topic_id)

        obj = DailyProgress.objects.create(
            teacher=request.user,
            topic=topic,
            date=date,
            lectures_covered=lectures,
            notes=notes,
            attachment=attachment
        )

        print("SAVED:", obj)

        return redirect('teacher_dashboard')

    return render(request, 'add_progress.html', {'topics': topics})
