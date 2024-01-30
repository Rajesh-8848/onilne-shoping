# your_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# your_app/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    # Add any additional fields or customizations if needed
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        help_text='Remember me'
    )

    # You can also override existing fields if needed
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'custom-class'  # Add a custom class to the username field

    # Add any additional methods or override existing methods as needed
    def clean_remember_me(self):
        # Custom validation for the remember_me field, if needed
        remember_me = self.cleaned_data.get('remember_me')
        if not remember_me:
            # Do something if remember_me is False
            pass

        return remember_me