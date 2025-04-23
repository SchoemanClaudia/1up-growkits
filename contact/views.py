from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

from .forms import ContactForm
from .models import ContactMessage


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Save message
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )

            # Send email
            subject = f"Contact Form Message from {name}"
            send_mail(
                subject,
                message,
                email,
                [settings.DEFAULT_FROM_EMAIL or 'noreply@1up-growkits.com']
            )

            # Redirect to message sent
            return redirect('message_sent')
    else:
        form = ContactForm()

    return render(request, 'contact/contact.html', {'form': form})


def message_sent(request):
    return render(request, 'contact/message_sent.html')
