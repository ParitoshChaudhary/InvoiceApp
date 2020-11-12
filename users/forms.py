from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate
from .models import UserAccount

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Required a valid email address.")

    class Meta:
        model = UserAccount
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserAccount.objects.get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError(f"Email {email} already in use. Please choose another one.")

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        try:
            account = UserAccount.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(f"Username {account} already in use. Please choose another one.")