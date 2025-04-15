from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse

from .models import Course
from .forms import CourseForm

# Create your views here.

def online_courses(request):
    """ A view to show available online courses for enrollment """

    courses = Course.objects.all()

    context = {
        'courses': courses,
    }

    return render(request, 'courses/courses.html', context)


def course_detail(request, course_id):
    """ A view to show individual online course details """

    course = get_object_or_404(Course, pk=course_id)

    context = {
        'course': course,
    }

    return render(request, 'courses/course_detail.html', context)


def add_course(request):
    """ Add a course to the store """
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES) 
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added course!')
            return redirect(reverse('courses')) 
        else:
            messages.error(request, 'Failed to add course. Please ensure the form is valid.')
    else:
        form = CourseForm() 

    context = {
        'form': form,
    }
    return render(request, 'courses/add_course.html', context) 
