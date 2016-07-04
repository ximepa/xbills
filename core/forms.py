# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django import forms
from .models import Admin, District, Street, House
import os


class LoginForm(forms.Form):
    #username = forms.CharField(widget=forms.Input(attrs={'size': '2', 'value': '1', 'class': 'input-small', 'maxlength': '5'}), error_messages={'invalid':_(u'Введите правильное количество')}, min_value=1, label=_(u'Количество'))
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError(_(u'Cookies должны быть включены'))
        return self.cleaned_data


class AdministratorForm(forms.ModelForm):
    disable = forms.BooleanField(required=False)

    class Meta:
        model = Admin
        fields = [
            'login',
            'name',
            'disable',
            'theme',
            'email',
            'address',
            'cell_phone',
            'phone',
        ]
        widgets = {
            'login': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Login'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Name'}),
            'disable': forms.CheckboxInput(),
            'theme': forms.Select(attrs={'class': 'form-control', 'placeholder': u'Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': u'Name'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Name'}),
            'cell_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Name'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Name'}),
        }


class SearchForm(forms.Form):
    district = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control input-sm', 'placeholder': u'District'}), queryset=District.objects.all())
    street = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control input-sm', 'placeholder': u'Street'}), queryset=Street.objects.all(), required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control input-sm', 'placeholder': u'House'}), queryset=House.objects.all(), required=False)