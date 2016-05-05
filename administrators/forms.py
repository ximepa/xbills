# -*- coding: utf-8 -*-
from django import forms
from administrators.models import CUser as User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm, AuthenticationForm


class UserCreationForm(AuthUserCreationForm):

    receive_newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username',
            # 'first_name',
            # 'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined'
        ]

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User._default_manager.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )


class UserChangeForm(AuthUserChangeForm):

    receive_newsletter = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username',
                  #'first_name',
                  #'last_name',
                  'email',
                  'is_staff',
                  'is_active',
                  'date_joined'
        ]


class CustomAuthenticationForm(AuthenticationForm):
    # add your form widget here
    username = forms.CharField(widget=forms.TextInput(attrs={}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))