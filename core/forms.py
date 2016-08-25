# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django import forms
from .models import Admin, District, Street, House, Group, User, Company
from django.db.models import Q
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
    DISABLED = (
       ('', _("All")),
       (0, _("Active")),
       (1, _("Disabled")),
       (2, _("Not Active")),
    )
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': u'Login'}))
    uid = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': u'UID'}))
    disabled = forms.ChoiceField(widget=forms.RadioSelect(), choices=DISABLED)
    district = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'ui search dropdown', 'placeholder': u'District'}), queryset=District.objects.all(), required=False)
    street = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'ui search dropdown', 'placeholder': u'Street'}), queryset=Street.objects.all(), required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'ui search dropdown', 'placeholder': u'House'}), queryset=House.objects.filter(~Q(number="")), required=False,)
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': u'Flat'}))


class SearchFeesForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': u'Login'}))
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control input-sm', 'placeholder': u'District'}), queryset=Group.objects.all(), required=False)


class SearchPaymentsForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control input-sm', 'placeholder': u'Login'}))
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'form-control input-sm', 'placeholder': u'District'}), queryset=Group.objects.all(), required=False)


class ClientForm(forms.ModelForm):
    gid = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'ui search dropdown'
            }
        )
    )

    # company = forms.ModelChoiceField(
    #     queryset=Company.objects.all(),
    #     empty_label=None,
    #     widget=forms.Select(
    #
    #     )
    # )

    class Meta:
        model = User
        fields = [
            'id',
            'login',
            'disabled',
            'company',
            'credit',
            'credit_date',
            'gid',
            'reduction',
            'reduction_date',
            'activate',
            'expire',
            'deleted',
            'registration',
            'bill',
        ]
        widgets = {
            'id': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'UID'}),
            'login': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'disabled': forms.CheckboxInput(attrs={'class': 'ui checkbox'}),
            'company': forms.Select(attrs={'class': 'ui dropdown'}),
            'credit': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Credit'}),
            'credit_date': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'reduction': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'reduction_date': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'activate': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Activation'}),
            'expire': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Expired'}),
            'deleted': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'registration': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'bill': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
        }
