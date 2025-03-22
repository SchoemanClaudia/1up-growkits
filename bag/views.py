from django.shortcuts import render, redirect, get_object_or_404
from courses.models import Course
from products.models import Product

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product or course to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # Differentiate items
    item_type = request.POST.get('item_type')

    bag = request.session.get('bag', {})

    # Determine if Product / Course
    if item_type == "course":
        item = get_object_or_404(Course, pk=item_id)
        # Course item indetifier
        item_key = f"course_{item_id}"
    else:
        item = get_object_or_404(Product, pk=item_id)
        # Product item indetifier
        item_key = f"product_{item_id}"

    if item_key in bag:
        bag[item_key] += quantity
    else:
        bag[item_key] = quantity

    request.session['bag'] = bag

    return redirect(redirect_url)


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def adjust_bag(request, item_id):
    """ Adjust qty of items added to shopping bag """
    
    item_type = request.POST.get('item_type')
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')

    bag = request.session.get('bag', {})

    item_key = f"{item_type}_{item_id}"

    if quantity > 0:
        bag[item_key] = quantity
    else:
        if item_key in bag:
            del bag[item_key]

    request.session['bag'] = bag
    return redirect(redirect_url)
