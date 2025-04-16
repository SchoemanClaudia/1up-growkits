from django.contrib import admin
from .models import Order, OrderLineItem
from .forms import OrderLineItemForm


class OrderLineItemAdminInline(admin.TabularInline):
    model = OrderLineItem
    form = OrderLineItemForm
    fields = ('item', 'quantity', 'lineitem_total')
    readonly_fields = ('lineitem_total',)
    can_delete = True
    extra = 0
    show_change_link = False


class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderLineItemAdminInline,)

    readonly_fields = (
        'order_number', 'date', 'delivery_cost',
        'order_total', 'grand_total', 'original_bag',
        'stripe_pid',
    )

    fields = (
        'order_number', 'user_profile', 'date', 'full_name', 'email',
        'phone_number', 'country', 'postcode',
        'town_or_city', 'street_address1', 'street_address2',
        'county', 'delivery_cost', 'order_total', 'grand_total', 
        'original_bag', 'stripe_pid', 'status',)

    list_display = (
        'order_number', 'date', 'full_name',
        'order_total', 'delivery_cost', 'grand_total', 'status',)
    
    list_filter = ('status',)

    ordering = ('-date',)

    class Media:
        js = ('checkout/js/admin_message.js',)


admin.site.register(Order, OrderAdmin)
