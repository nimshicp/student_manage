from django.shortcuts import render,redirect, get_object_or_404
from .models import Student
from .forms import StudentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .models import Student
from django.core.paginator import Paginator




def student_list(request):
    students = Student.objects.all().order_by('roll_no').prefetch_related('courses')

    search = request.GET.get('search')
    if search:
        students = students.filter(
            Q(name__icontains=search) |
            Q(roll_no__icontains=search) |
            Q(courses__title__icontains=search)
        ).distinct()

    paginator = Paginator(students, 4)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'student_list.html', {
        'students': page_obj,     
        'page_obj': page_obj
    })



@login_required
def student_add(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)

        if form.is_valid():
            email = form.cleaned_data['email'].strip().lower()
            name = form.cleaned_data['name']

            
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email already exists.")
                return render(request, 'student_add.html', {'form': form})

            
            user = User.objects.create(
                username=email,
                email=email,
                first_name=name,
                is_active=True
            )
            user.set_unusable_password()
            user.save()   

            
            student, _ = Student.objects.get_or_create(user=user)
            student.name = name
            student.email = email
            student.save()

            
            try:
                send_mail(
                    subject='Complete Your Registration',
                    message=(
                        f"Hi {name},\n\n"
                        f"You have been added to the Student Management System.\n\n"
                        f"Please register using this email:\n{email}\n\n"
                        f"After registration, you can log in.\n\n"
                        f"Thank you."
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception:
                messages.warning(
                    request,
                    "Student added, but email could not be sent."
                )

            messages.success(
                request,
                "Student added successfully. Invitation email sent."
            )
            return redirect('students:student_list')

    else:
        form = StudentForm()

    return render(request, 'student_add.html', {'form': form})


@login_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
            form.save_m2m()   
            messages.success(request, "Student updated successfully")
            return redirect('students:student_list')
    else:
        form = StudentForm(instance=student)

    return render(request, 'student_add.html', {
        'form': form,
        'title': 'Edit Student'
    })



@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'POST':
        
        user = student.user 
        
        
        if user:
            user.delete()
        else:
            
            student.delete()
        
        messages.success(request, "Student and associated user account deleted successfully")
        return redirect('students:student_list')

    return render(request, 'student_delete.html', {
        'student': student
    })

@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    return render(request, 'student_detail.html', {
        'student': student
    })



