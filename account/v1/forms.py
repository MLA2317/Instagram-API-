from django import forms
from account.models import Account
from django.contrib.auth.forms import UserCreationForm


class AccountRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Username'}), max_length=220, required=True)
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), max_length=20, required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), max_length=20, required=False)
    date_of_birth = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'input', 'placeholder': 'Date of birth', 'type': 'date'}), required=False)
    gender = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Gender'}), required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter Password', 'class': 'prompt srch_explore'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'prompt srch_explore'}))

    class Meta:
        model = Account
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'gender', 'email', 'bio', 'phone_number',
                  'avatar', 'location', 'password', 'password2']


class EditProfileForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}), required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}), required=True)
    date_of_birth = forms.DateTimeField(widget=forms.DateInput(attrs={'class': 'input', 'placeholder': 'Date of birth', 'type': 'date'}),required=False)
    bio = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Bio'}), required=True)
    gender = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Gender'}), required=False)
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Email'}), required=True)
    avatar = forms.ImageField(required=True)
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Address'}), required=True)
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Phone Number'}), required=True)

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'date_of_birth', 'bio', 'gender', 'email', 'avatar', 'location', 'phone_number']
