from django.shortcuts import render
from .models import GrowGuide

# Create your views here.


def grow_guide(request):
    guide = GrowGuide.objects.all()

    context = {
        'guide': guide,
    }

    return render(request, 'guide/grow_guide.html', {'guide': guide})
    