from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import TeacherLoginForm, StudentLoginForm


# ✅ Teacher Login
def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            return render(request, 'teacher_login.html', {'error': 'Invalid credentials'})

    return render(request, 'teacher_login.html')

# ✅ Student Login
def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('student_dashboard')
        else:
            return render(request, 'student_login.html', {'error': 'Invalid credentials'})

    return render(request, 'student_login.html')

# user login
def user_login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # 🔥 Role-based redirect
            if user.role == 'Teacher':
                return redirect('teacher_dashboard')

            elif user.role == 'Student':
                return redirect('student_dashboard')

            elif user.role == 'Admin':
                return redirect('/admin/')

            elif user.role == 'Principal':
                return redirect('teacher_dashboard')  # for now

        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')