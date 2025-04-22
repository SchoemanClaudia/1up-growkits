from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm
from django.conf import settings

# Create your views here.


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f"Contact Form Message from {form.cleaned_data['name']}"
            message = form.cleaned_data['message']
            from_email = form.cleaned_data['email']
            send_mail(subject, message, from_email, [settings.DEFAULT_FROM_EMAIL])
            messages.success(request, "Your message has been sent!")
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})
