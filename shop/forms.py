# shop/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML
User = get_user_model()
# nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
# SIGN-UP FORM
# nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
class SignUpForm(UserCreationForm):
    email      = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name  = forms.CharField(max_length=50)
    newsletter = forms.BooleanField(required=False,
                     label='Subscribe to our newsletter')
    class Meta:
        model  = User
        fields = [
            'username', 'email', 'first_name', 'last_name',
            'password1', 'password2', 'newsletter',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name',  css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Field('username',   css_class='form-control'),
            Field('email',      css_class='form-control'),
            Field('password1',  css_class='form-control'),
            Field('password2',  css_class='form-control'),
            Field('newsletter'),
            Submit('submit', 'Create Account',
                   css_class='btn btn-primary btn-block mt-3'),
            HTML('<p class="mt-3 text-center">',
                 'Already have an account? '
                 '<a href="{% url \'shop:login\' %}">Login</a></p>'),
        )
        def clean_email(self):
           email = self.cleaned_data['email'].lower()
           if User.objects.filter(email=email).exists():
               raise forms.ValidationError('This email is already registered.')
           return email
# nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
# LOGIN FORM
# nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
class LoginForm(AuthenticationForm):
    """Extends Django's built-in form to add crispy layout."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('username', css_class='form-control',
                  placeholder='Email or username'),
            Field('password', css_class='form-control',
                  placeholder='Password'),
            Submit('submit', 'Log In',
                   css_class='btn btn-success btn-block mt-3'),
            HTML(
                '<div class="text-center mt-2">'
                '<a href="{% url \'password_reset\' %}">'
                'Forgot password?</a></div>'
            ),
        )
# nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
# PROFILE UPDATE FORM
# nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = [
            'first_name', 'last_name', 'email',
            'phone', 'avatar',
            'address', 'city', 'postal_code', 'country',
            'newsletter',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.attrs = {'enctype': 'multipart/form-data'}
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='col-md-6'),
                Column('last_name',  css_class='col-md-6'),
            ),
            'email', 'phone', 'avatar',
            HTML('<hr><h5 class="mt-2">Shipping Address</h5>'),
            'address',
            Row(
                Column('city',        css_class='col-md-4'),
                Column('postal_code', css_class='col-md-4'),
                Column('country',     css_class='col-md-4'),
            ),
            'newsletter',
            Submit('submit', 'Save Changes',
                   css_class='btn btn-primary mt-3'),
        )
        
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, Submit


SUBJECT_CHOICES = [
    ('order',   'Order & Shipping'),
    ('return',  'Returns & Refunds'),
    ('product', 'Product Question'),
    ('account', 'Account & Payments'),
    ('other',   'Other'),
]


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'John Doe'}),
        error_messages={'required': 'Please enter your name.'},
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'}),
        error_messages={
            'required': 'Please enter your email address.',
            'invalid':  'Enter a valid email address.',
        },
    )
    subject = forms.ChoiceField(
        choices=[('', 'Select a topic…')] + SUBJECT_CHOICES,
        error_messages={'required': 'Please select a subject.'},
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows':        6,
            'placeholder': 'Tell us how we can help…',
        }),
        error_messages={'required': 'Please enter a message.'},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action = 'shop:contact'
        self.helper.layout = Layout(
            Row(
                Column('name',  css_class='form-group col-md-6'),
                Column('email', css_class='form-group col-md-6'),
                css_class='form-row',
            ),
            Field('subject', css_class='form-group'),
            Field('message', css_class='form-group'),
            Submit('submit', 'Send Message', css_class='btn btn-primary btn-lg px-5'),
        )
