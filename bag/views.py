from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from courses.models import Course
from products.models import Product

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product or course to the shopping bag """

    try:
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
            item_name = item.title
        else:
            item = get_object_or_404(Product, pk=item_id)
            # Product item indetifier
            item_key = f"product_{item_id}"
            item_name = item.name

        if quantity <= 0:
            messages.error(request, "Quantity must be at least 1")
            return redirect(redirect_url)

        if item_key in bag:
            bag[item_key] += quantity
            messages.success(request, f'Updated with x{quantity} {item_name}')
        else:
            bag[item_key] = quantity
            messages.success(request, f'Added {item_name} to your bag')

        request.session['bag'] = bag
        return redirect(redirect_url)

    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity")
        return redirect(request.POST.get('redirect_url', 'view_bag'))

    except Exception as e:
        messages.error(request, "Something went wrong while adding to your bag")

        return redirect(request.POST.get('redirect_url', 'view_bag'))


def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')


def adjust_bag(request, item_id):
    """ Adjust qty of items added to shopping bag """

    try:
        quantity = int(request.POST.get('quantity'))
        item_type = request.POST.get('item_type')
        redirect_url = request.POST.get('redirect_url')

        bag = request.session.get('bag', {})

        item_key = f"{item_type}_{item_id}"

        if item_type == "course":
            item = get_object_or_404(Course, pk=item_id)
            item_name = item.title
        else:
            item = get_object_or_404(Product, pk=item_id)
            item_name = item.name

        if quantity > 0:
            bag[item_key] = quantity
            messages.success(request, f'Updated with x{quantity} {item_name}')
        else:
            if item_key in bag:
                del bag[item_key]
                messages.success(request, f'Removed {item_name} from your bag')

        request.session['bag'] = bag
        return redirect(redirect_url)

    except (TypeError, ValueError):
        messages.error(request, "Invalid quantity submitted")
        return redirect(request.POST.get('redirect_url', 'view_bag'))

    except Exception as e:
        messages.error(request, "Something went wrong while updating your bag")

        return redirect(request.POST.get('redirect_url', 'view_bag'))
