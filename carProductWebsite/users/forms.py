from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser

from django.contrib.auth import get_user_model
User = get_user_model()



class CustomUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        print("VAMOS A GUARDAR")
        user = super(CustomUserForm, self).save()
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user