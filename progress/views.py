from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import DailyProgress
from courses.models import Topic
from accounts.decorators import teacher_required
from .models import ChatMessage
from courses.models import Enrollment
from courses.models import Course
from django.contrib.auth import get_user_model
User = get_user_model()
from django.http import JsonResponse
from .models import ChatMessage
from django.utils import timezone
import pytz
from .models import Complaint


@login_required
@teacher_required
def add_progress(request):

    # Show only topics (you can later filter by teacher if needed)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        progress_date = request.POST.get('date')
        lectures = request.POST.get('lectures')
        notes = request.POST.get('notes')
        attachment = request.FILES.get('attachment')

        #  Basic validation
        if not topic_id or not progress_date:
            messages.error(request, "Please fill all required fields ❌")
            return render(request, 'add_progress.html', {'topics': topics})

        try:
            topic = Topic.objects.get(id=topic_id)
        except Topic.DoesNotExist:
            messages.error(request, "Invalid topic selected ❌")
            return render(request, 'add_progress.html', {'topics': topics})

        #  Save data
        DailyProgress.objects.create(
            teacher=request.user,
            topic=topic,
            date=progress_date,
            lectures_covered=lectures or 0,   # prevent empty crash
            notes=notes or '',
            attachment=attachment
        )

        messages.success(request, "Progress added successfully ✅")
        return redirect('teacher_dashboard')

    return render(request, 'add_progress.html', {'topics': topics})

#  Student: Course select page
@login_required
def chat_select(request):

    enrollments = Enrollment.objects.filter(student=request.user)

    return render(request, 'chat_select.html', {
        'enrollments': enrollments
    })


# Teacher: Student list
@login_required
def teacher_chat(request):

    # teacher ke courses
    courses = Course.objects.filter(teacher=request.user)

    # un courses ke students
    enrollments = Enrollment.objects.filter(course__in=courses)

    students = User.objects.filter(
        id__in=enrollments.values_list('student_id', flat=True)
    ).distinct()

    return render(request, 'teacher_chat.html', {
        'students': students
    })

#  Chat room
@login_required
def chat_room(request, user_id):

    receiver = User.objects.get(id=user_id)

    messages = ChatMessage.objects.filter(
        sender=request.user, receiver=receiver
    ) | ChatMessage.objects.filter(
        sender=receiver, receiver=request.user
    )

    messages = messages.order_by('timestamp')

    if request.method == 'POST':
        msg = request.POST.get('message')

        if msg:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                message=msg
            )
            return redirect('chat_room', user_id=user_id)

    return render(request, 'chat_room.html', {
        'messages': messages,
        'receiver': receiver
    })


@login_required
def get_messages(request, user_id):

    messages = ChatMessage.objects.filter(
        sender=request.user, receiver_id=user_id
    ) | ChatMessage.objects.filter(
        sender_id=user_id, receiver=request.user
    )

    messages = messages.order_by('timestamp')

    ist = pytz.timezone('Asia/Kolkata')

    data = []

    for msg in messages:

        local_time = timezone.localtime(msg.timestamp, ist)

        data.append({
            'message': msg.message,
            'sender': msg.sender.username,
            'is_me': True if msg.sender == request.user else False,
            'time': local_time.strftime("%I:%M %p"),
            'date': local_time.strftime("%d %b %Y")
        })

    return JsonResponse({'messages': data})

from django.contrib import messages

@login_required
def submit_complaint(request):

    if request.method == 'POST':
        msg = request.POST.get('message')

        Complaint.objects.create(
            student=request.user,
            message=msg
        )

        messages.success(request, "Complaint submitted successfully!")

        return redirect('submit_complaint')

    complaints = Complaint.objects.filter(student=request.user).order_by('-created_at')

    return render(request, 'submit_complaint.html', {
        'complaints': complaints
    })
