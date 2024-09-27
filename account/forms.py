from typing import Any
from .models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterForm(UserCreationForm):
    # Add additional fields here, such as email or phone number
    class Meta:
        model = User
        fields = ( 'first_name', 'last_name', 'email', 'password1', 'password2')
        help_texts = {
            'username': 'Your username must be unique.',
            'email': 'Please enter a valid email address.',
            'phone_number': 'Please enter a valid phone number.',
        }
    
    
class LoginForm(AuthenticationForm):
    # Add additional fields here, such as remember me checkbox
    username = forms.EmailField(widget=forms.EmailInput())
    class Meta:

        fields = ( 'username', 'password')
        help_texts = {
            'email': 'Please enter a valid email address.',
        }
        
class ProfileImageChangeForm(forms.ModelForm):
    profile_image = forms.FileField(widget=forms.FileInput(attrs={'required' : True}))
    class Meta:
        model = User
        fields = ('profile_image',)

    def clean(self):
        cleaned_data =  super().clean()
        image = cleaned_data.get('profile_image')
        if image: 
            if image.size > 150 * 1024:
                self.add_error('profile_image', 'Image should be less than 100 kb')


        return cleaned_data