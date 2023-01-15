from django import forms
from django.core.exceptions import ValidationError
from datetime import datetime
from app import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=1, max_length=25)
    password = forms.CharField(min_length=1, max_length=25, widget=forms.PasswordInput)
