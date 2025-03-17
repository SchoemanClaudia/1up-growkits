from django.shortcuts import render
from .models import Course, Enrollment

# Create your views here.

def online_courses(request):
    """ A view to show available online courses for enrollment """

    courses = Course.objects.all()

    context = {
        'courses': courses,
    }

    return render(request, 'courses/courses.html', context)