from django.contrib import admin
from .models import Order, OrderLineItem

# Register your models here.

class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    fields = ('product', 'course', 'quantity', 'lineitem_total')
    readonly_fields = ('lineitem_total',)
    can_delete = True
    extra = 0
    show_change_link = False

    # Field to display product or course
    def display_item(self, obj):
        """ Show either product or course name """
        if obj.product:
            return f"Product: {obj.product.name}"
        elif obj.course:
            return f"Course: {obj.course.title}"
        return "—"
    display_item.short_description = 'Item'


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'delivery_cost',
        'order_total', 'grand_total',
    )

    fields = (
        'order_number', 'date', 'full_name', 'email',
        'phone_number', 'country', 'postcode',
        'town_or_city', 'street_address1', 'street_address2',
        'county', 'delivery_cost', 'order_total', 'grand_total',
    )

    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'delivery_cost', 'grand_total',
    )

    ordering = ('-date',)

    class Media:
        js = ('checkout/js/admin_message.js',)

admin.site.register(Order, OrderAdmin)
