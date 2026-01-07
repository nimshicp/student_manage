
from django.shortcuts import render,redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

def course_list(request):
    courses = Course.objects.all().order_by('title')

    search = request.GET.get('search')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) 
        )

    paginator = Paginator(courses, 4)   
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'course_list.html', {
        'courses': page_obj,
        'page_obj': page_obj
    })

@login_required
def course_add(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Course added successfully")
            return redirect('courses:course_list')
    else:
        form = CourseForm()

    return render(request, 'course_add.html', {
        'form': form,
        'title': 'Add Course'
    })


@login_required
def course_edit(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully")
            return redirect('courses:course_list')
    else:
        form = CourseForm(instance=course)

    return render(request, 'course_add.html', {
        'form': form,
        'title': 'Edit Course'
    })

@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        course.delete()
        messages.success(request, "Course deleted successfully")
        return redirect('courses:course_list')

    return render(request, 'course_delete.html', {'course': course})

