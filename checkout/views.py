from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

# Create your views here.

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))
    
    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51R5ubmRJMn2CInf7jsU7o0IqvCUQKw9Zr8xo32htBsQaB0tXBQiKDc04kPtQsouIBmB0ymH2IRtZrapXrNI49xC500EPyUjTc5',
        'client_secret': 'test client secret',
    }

    return render(request, template, context)