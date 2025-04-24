from django.shortcuts import render
from .models import GrowGuide


def grow_guide(request):
    """
    A view to display mushroom grow kit guide.
    Previews all guide steps and passes them to template in order.
    """
    guide = GrowGuide.objects.all()

    context = {
        'guide': guide,
    }

    return render(request, 'guide/grow_guide.html', context)
