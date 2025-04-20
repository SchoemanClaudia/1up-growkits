from django.shortcuts import render
from products.models import Product

# Create your views here.

def index(request):
    """ A view to return the index page with featured products """
    
    featured_products = Product.objects.filter(featured=True)[:3]

    context = {
        'featured_products': featured_products,
    }

    return render(request, 'home/index.html', context)