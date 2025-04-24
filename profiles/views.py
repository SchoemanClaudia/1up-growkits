from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import UserProfile
from .forms import UserProfileForm

from checkout.models import Order


@login_required
def profile(request):
    """
    Display and handle updates to user profile.
    Allows users to update their default delivery information
    and display user's order history.
    """
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save()

            # Sync with Django User model
            user = request.user
            user.first_name = profile.default_first_name or ''
            user.last_name = profile.default_last_name or ''
            user.save()

            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(
                request,
                'Update failed. Please ensure the form is valid.'
            )
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    context = {
        'form': form,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, 'profiles/profile.html', context)


def order_history(request, order_number):
    """
    Display past order info from the user profile page.
    Allows users to view order history details.
    """
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(
        request,
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    )

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
