from django import forms
from .widgets import CustomClearableFileInput
from .models import Course
from django.forms.widgets import DateTimeInput


class CustomDateTimeInput(DateTimeInput):
    input_type = 'datetime-local'
    format = '%Y-%m-%dT%H:%M'


class CourseForm(forms.ModelForm):
    """
    Form for creating and editing Course instances.
    Uses a custom widget for image input.
    """
    class Meta:
        model = Course
        fields = '__all__'
        widgets = {
            'start_datetime': CustomDateTimeInput(attrs={
                'class': 'form-control',
            }),
        }

    image = forms.ImageField(
        label='Image',
        required=False,
        widget=CustomClearableFileInput
    )

    def __init__(self, *args, **kwargs):
        """
        Add consistent styling to all fields using CSS classes
        """
        super().__init__(*args, **kwargs)

        # Apply the class to all fields
        for field_name, field in self.fields.items():
            if field_name != 'start_datetime':  # Already styled in widget
                field.widget.attrs['class'] = 'border-black rounded-0'

        # Show datetime field with correct format
        if self.instance and self.instance.start_datetime:
            self.fields['start_datetime'].initial = self.instance.start_datetime.strftime('%Y-%m-%dT%H:%M')
