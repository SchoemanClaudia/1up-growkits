from django.shortcuts import (
    render, redirect, reverse, get_object_or_404, HttpResponse
)
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth import REDIRECT_FIELD_NAME

from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from courses.models import Course, Enrollment
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from bag.contexts import bag_contents

import stripe
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'bag': json.dumps(request.session.get('bag', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            'Sorry, your payment cannot be processed right now. '
            'Please try again later.'
        )
        return HttpResponse(content=e, status=400)


def checkout(request):
    if not request.user.is_authenticated:
        messages.warning(
            request,
            "Please log in to continue with your order."
        )
        return redirect(
            f'{settings.LOGIN_URL}?{REDIRECT_FIELD_NAME}={request.path}'
        )

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        bag = request.session.get('bag', {})

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_bag = json.dumps(bag)

            if request.user.is_authenticated:
                order.user_profile = UserProfile.objects.get(
                    user=request.user
                )

            order.save()

            for item_key, quantity in bag.items():
                item_type, item_id = item_key.split('_')
                try:
                    if item_type == 'product':
                        product = get_object_or_404(Product, pk=item_id)
                        OrderLineItem.objects.create(
                            order=order,
                            product=product,
                            quantity=quantity,
                        )
                    elif item_type == 'course':
                        course = get_object_or_404(Course, pk=item_id)
                        OrderLineItem.objects.create(
                            order=order,
                            course=course,
                            quantity=quantity,
                        )
                except (Product.DoesNotExist, Course.DoesNotExist):
                    messages.error(
                        request,
                        "An item in your bag wasn't found. "
                        "Please contact support."
                    )
                    order.delete()
                    return redirect(reverse('view_bag'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(
                reverse('checkout_success', args=[order.order_number])
            )
        else:
            messages.error(
                request,
                'There was an error with your form. '
                'Please double check your information.'
            )

    else:
        bag = request.session.get('bag', {})
        if not bag:
            messages.error(
                request,
                "There's nothing in your bag at the moment"
            )
            return redirect(reverse('products'))

        current_bag = bag_contents(request)
        total = current_bag['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        try:
            profile = UserProfile.objects.get(user=request.user)
            order_form = OrderForm(initial={
                'full_name': profile.user.get_full_name(),
                'email': profile.user.email,
                'phone_number': profile.default_phone_number,
                'country': profile.default_country,
                'postcode': profile.default_postcode,
                'town_or_city': profile.default_town_or_city,
                'street_address1': profile.default_street_address1,
                'street_address2': profile.default_street_address2,
                'county': profile.default_county,
            })
        except UserProfile.DoesNotExist:
            order_form = OrderForm()

        if not stripe_public_key:
            messages.warning(
                request,
                'Stripe public key is missing. '
                'Did you forget to set it in your environment?'
            )

        template = 'checkout/checkout.html'
        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        return render(request, template, context)


def checkout_success(request, order_number):
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        order.user_profile = profile
        order.save()

        if save_info:
            profile_data = {
                'default_phone_number': order.phone_number,
                'default_country': order.country,
                'default_postcode': order.postcode,
                'default_town_or_city': order.town_or_city,
                'default_street_address1': order.street_address1,
                'default_street_address2': order.street_address2,
                'default_county': order.county,
            }
            user_profile_form = UserProfileForm(
                profile_data,
                instance=profile
            )
            if user_profile_form.is_valid():
                user_profile_form.save()

    lineitems = order.lineitems.all()
    for item in lineitems:
        if item.product:
            product = item.product
            if product.stock_quantity >= item.quantity:
                product.stock_quantity -= item.quantity
                product.save()

        elif item.course:
            course = item.course
            user = request.user if request.user.is_authenticated else None

            already_enrolled = Enrollment.objects.filter(
                course=course, order=order, user=user
            ).exists()

            if user and not already_enrolled:
                enrollment = Enrollment.objects.create(
                    course=course,
                    user=user,
                    order=order,
                    enrolled_at=order.date,
                    is_paid=True,
                    confirmed=False,
                    status=Enrollment.PENDING,
                    spots_booked=item.quantity,
                )
                enrollment.send_course_email()

    subject = render_to_string(
        'checkout/confirmation_emails/confirmation_email_subject.txt',
        {'order': order, 'user': request.user}
    ).strip()

    body = render_to_string(
        'checkout/confirmation_emails/confirmation_email_body.txt',
        {'order': order, 'user': request.user}
    )

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
    )

    messages.success(
        request,
        f'Order successfully processed! '
        f'Your order number is {order_number}. '
        f'A confirmation email will be sent to {order.email}.'
    )

    if 'bag' in request.session:
        del request.session['bag']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)
