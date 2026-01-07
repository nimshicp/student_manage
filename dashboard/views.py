
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from students.models import Student
from courses.models import Course

@login_required
def dashboard_view(request):
    profile = request.user.profile

  
    if profile.role == 'ADMIN':
        total_students = Student.objects.count()
        total_courses = Course.objects.count()

        return render(request, 'admin_dashboard.html', {
            'total_students': total_students,
            'total_courses': total_courses,
        })

    student, created = Student.objects.get_or_create(
        user=request.user,
        defaults={
            "roll_no": request.user.username,
            "name": request.user.username,
            "year_of_admission": 2024
        }
    )

    return render(request, 'student_dashboard.html', {
        'student': student
    })
