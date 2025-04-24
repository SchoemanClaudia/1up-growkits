from django import forms
from .widgets import CustomClearableFileInput
from .models import Course


class CourseForm(forms.ModelForm):
    """
    Form for creating and editing Course instances.
    Uses a custom widget for image input.
    """
    class Meta:
        model = Course
        fields = '__all__'

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

        # Apply the class to the fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
