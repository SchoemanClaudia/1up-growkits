from django.shortcuts import render
from .models import GrowGuide


def grow_guide(request):
    guide = GrowGuide.objects.all()

    context = {
        'guide': guide,
    }

    return render(request, 'guide/grow_guide.html', context)
