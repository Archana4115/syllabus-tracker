from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import csv

from courses.models import Course   # ✅ ONLY THIS


# 👨‍🏫 TEACHER REPORT
@login_required
def teacher_report(request):

    courses = Course.objects.all()

    return render(request, 'report/teacher_report.html', {
        'courses': courses
    })


# 👨‍🎓 STUDENT REPORT
@login_required
def student_report(request):

    courses = Course.objects.all()

    return render(request, 'report/student_report.html', {
        'courses': courses
    })


# 📄 DOWNLOAD REPORT
@login_required
def download_report(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Course Name'])

    courses = Course.objects.all()

    for c in courses:
        writer.writerow([c.course_name])   # ✅ ONLY NAME (NO completion)

    return response


from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def send_email_view(request):

    students = User.objects.exclude(id=request.user.id)
   
    if request.method == 'POST':

        student_id = request.POST.get('student')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        student = User.objects.get(id=student_id)

        send_mail(
            subject,
            message,
            'your_email@gmail.com',
            [student.email],
            fail_silently=False,
        )

        messages.success(request, "Email sent successfully ✅")

    return render(request, 'report/send_email.html', {
        'students': students
    })