from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SearchForm (forms.Form):
    query = forms.CharField(label='Search', max_length=100)
    filter = forms.IntegerField()

class SignUpForm(UserCreationForm):
    username= forms.CharField(max_length=30, label='Username:')
    email = forms.EmailField(max_length=200,label='Email:')
    first_name = forms.CharField(max_length=100,label='First Name:', )
    last_name = forms.CharField(max_length=100,label='Last Name:', )
    # password1 = forms.CharField(max_length=100,label='Password:', help_text='Password')
    # password2 = forms.CharField(max_length=100,label='Password(Again):', help_text='Password (Again): ')

    class Meta:
        model= User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
