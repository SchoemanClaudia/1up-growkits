from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(label="Your Email")
    message = forms.CharField(widget=forms.Textarea, label="Your Message")

    def __init__(self, *args, **kwargs):
        """
        Initialize contact form with Crispy Forms helper:
        - Set form method and classes
        - Apply layout styling with Bootstrap spacing
        """
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'contact-form'
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Field('name', css_class='mb-3'),
            Field('email', css_class='mb-3'),
            Field('message', css_class='mb-4'),
            Submit(
                'submit',
                'Send Message',
                css_class='btn btn-shop btn-lg w-100 rounded-0 text-uppercase'
            )
        )
