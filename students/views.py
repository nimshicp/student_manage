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

            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.")
                return render(request, 'student_add.html', {'form': form, 'title': "Add Student"})

            
            base_name = form.cleaned_data['name'].strip().lower().replace(" ", "")
            default_password = f"{base_name}@123"
            user = User.objects.create_user(username=email, email=email, password=default_password)

            
            try:
                student_instance = Student.objects.get(user=user)
            except Student.DoesNotExist:
                
                user.delete()
                messages.error(request, "System error: Failed to initialize student profile. Please try again.")
                return render(request, 'student_add.html', {'form': form, 'title': "Add Student"})
            
        
            form = StudentForm(request.POST, request.FILES, instance=student_instance)
            
        
            if form.is_valid():
                student = form.save() 
            else:
                user.delete() 
                return render(request, 'student_add.html', {'form': form, 'title': "Add Student"})

            
            try:
                send_mail(
                    subject='Student Account Created',
                    message=(
                        f"Hi {student.name},\n\n"
                        f"Your account: {email}\n"
                        f"Password: {default_password}"
                    ),
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception:
                messages.warning(request, "Student added, but email failed.")

            messages.success(request, "Student added successfully.")
            return redirect('students:student_list')

    else:
        form = StudentForm()

    return render(request, 'student_add.html', {'form': form, 'title': "Add Student"})



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



