from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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


@login_required
def add_course(request):
    """ Add a course to the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES) 
        if form.is_valid():
            course = form.save()
            messages.success(request, 'Successfully added course!')
            return redirect(reverse('course_detail', args=[course.id]))
        else:
            messages.error(request, 'Failed to add course. Please ensure the form is valid.')
    else:
        form = CourseForm() 

    context = {
        'form': form,
    }
    return render(request, 'courses/add_course.html', context) 

@login_required
def edit_course(request, course_id):
    """ Edit a course in the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated course!')
            return redirect(reverse('course_detail', args=[course.id]))
        else:
            messages.error(request, 'Failed to update course. Please ensure the form is valid.')
    else:
        form = CourseForm(instance=course)
        messages.info(request, f'You are editing {course.title}')

    template = 'courses/edit_course.html'
    context = {
        'form': form,
        'course': course,
    }

    return render(request, template, context)

@login_required
def delete_course(request, course_id):
    """ Delete a course from the store """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    messages.success(request, 'Course deleted!')
    return redirect(reverse('courses'))

