from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product
from courses.models import Course

def bag_contents(request):
    bag_items = []
    total = 0
    product_count = 0
    bag = request.session.get('bag', {})

    for item_key, quantity in bag.items():
        # Product handler
        if item_key.startswith("product_"):
            item_id = item_key.split("_", 1)[1]
            try:
                item_id = int(item_id)
                product = get_object_or_404(Product, pk=item_id)
            except (ValueError, Product.DoesNotExist):
                continue # Skip invalid product id

            subtotal = quantity * product.price 
            total += subtotal
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': product,
                'subtotal': subtotal, 
                'type': 'product',
            })

        # Course handler
        elif item_key.startswith("course_"):
            item_id = item_key.split("_", 1)[1]
            try:
                item_id = int(item_id)
                course = get_object_or_404(Course, pk=item_id)
            except (ValueError, Course.DoesNotExist):
                continue  # Skip invalid course id

            subtotal = quantity * course.price 
            total += subtotal
            product_count += quantity
            bag_items.append({
                'item_id': item_id,
                'quantity': quantity,
                'product': course,
                'subtotal': subtotal, 
                'type': 'course',
            })

    # Only calculate delivery for physical products
    physical_total = sum(item['subtotal'] for item in bag_items if item['type'] == 'product')

    if 0 < physical_total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = physical_total * Decimal(settings.STANDARD_DELIVERY_PERCENTAGE / 100)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - physical_total
    else:
        delivery = Decimal('0.00')
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'bag_items': bag_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
