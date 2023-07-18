
from django import forms
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from .models import GalleryModel, Blog

class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100,  help_text='Required', required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email = email).exists():
            raise ValidationError("User with the same email already exists")
        return email

    
class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50)


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'newpassword2']


class GalleryForm(forms.ModelForm):
    class Meta:
        model = GalleryModel
        fields = ['title', 'description', 'image']



class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog    
        fields = ['title', 'content', 'image']







        