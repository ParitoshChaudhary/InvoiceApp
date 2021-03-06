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


class AccountAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = UserAccount
        fields = ["username", "password"]

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data['password']
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid Login")


class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields = ['username', 'email', 'profile_pic', 'company_name']

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = UserAccount.objects.exclude(pk=self.instance.pk).get(email=email)
        except ObjectDoesNotExist:
            return email
        raise forms.ValidationError(f'Email {email} already in use')

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            account = UserAccount.objects.exclude(pk=self.instance.pk).get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError(f"Username {username} already exists")

    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email']
        account.profile_pic = self.cleaned_data['profile_pic']
        account.company_name = self.cleaned_data['company_name']
        if account:
            account.save() 
        return account