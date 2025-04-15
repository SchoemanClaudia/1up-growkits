from django.shortcuts import render, get_object_or_404
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
    form = CourseForm()
    template = 'courses/add_course.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
