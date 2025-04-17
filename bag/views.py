from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
            
            # Prevent overbooking
            spaces_left = item.spaces_left
            existing_in_bag = bag.get(item_key, 0)

            if quantity + existing_in_bag > spaces_left:
                allowed = max(0, spaces_left - existing_in_bag)
                messages.error(request, f"Only {allowed} spot(s) left for {item.title}.")
                return redirect(redirect_url)

        else:
            item = get_object_or_404(Product, pk=item_id)
            # Product item indetifier
            item_key = f"product_{item_id}"
            item_name = item.name

            existing_in_bag = bag.get(item_key, 0)
            if quantity + existing_in_bag > item.stock_quantity:
                allowed = max(0, item.stock_quantity - existing_in_bag)
                messages.error(request, f"Only {allowed} of {item.name} left in stock.")
                return redirect(redirect_url)

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

        # Course
        if item_type == "course":
            item = get_object_or_404(Course, pk=item_id)
            item_name = item.title
            spaces_left = item.spaces_left

            if quantity > 0:
                if quantity > spaces_left:
                    messages.error(request, f"Only {spaces_left} spot(s) available for {item_name}.")
                    return redirect(redirect_url)
                bag[item_key] = quantity
                messages.success(request, f'Updated with x{quantity} {item_name}')
            else:
                if item_key in bag:
                    del bag[item_key]
                    messages.success(request, f'Removed {item_name} from your bag')

        # Product
        else:
            item = get_object_or_404(Product, pk=item_id)
            item_name = item.name

            if quantity > 0:
                if quantity > item.stock_quantity:
                    messages.error(request, f"Only {item.stock_quantity} of {item_name} left in stock.")
                    return redirect(redirect_url)
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
