from django import forms

from .models import Order
from .models import OrderLineItem

from products.models import Product
from courses.models import Course


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


class OrderLineItemForm(forms.ModelForm):
    item = forms.ChoiceField(label='Item', required=True)

    class Meta:
        model = OrderLineItem
        fields = ('item', 'quantity')

    def __init__(self, *args, **kwargs):
        """
        Update item field to include both product and course items.
        Sets the initial value if editing an existing instance.
        """
        super().__init__(*args, **kwargs)

        # Combined dropdown options
        product_choices = [
            (f'product_{p.id}', f'Product: {p.name}')
            for p in Product.objects.all()
        ]
        course_choices = [
            (f'course_{c.id}', f'Course: {c.title}')
            for c in Course.objects.all()
        ]
        self.fields['item'].choices = product_choices + course_choices

        instance = kwargs.get('instance')
        if instance:
            if instance.product:
                self.fields['item'].initial = f'product_{instance.product.id}'
            elif instance.course:
                self.fields['item'].initial = f'course_{instance.course.id}'

    def save(self, commit=True):
        """
        Divide selected item into type and ID, clear previous fields,
        assign correct related product/course before saving.
        """
        item_type, item_id = self.cleaned_data['item'].split('_')

        # Clear fields before allocating item
        self.instance.product = None
        self.instance.course = None

        # Assign selected item
        if item_type == 'product':
            self.instance.product = Product.objects.get(id=item_id)
        elif item_type == 'course':
            self.instance.course = Course.objects.get(id=item_id)

        return super().save(commit=commit)
