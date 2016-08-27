# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django import forms
from .models import Admin, District, Street, House, Group, User, Company, Dv, Tp, UserPi
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
            'disabled': forms.CheckboxInput(attrs={'class': 'ui checkbox', 'onclick': 'ipdhcp_disable'}),
            'company': forms.Select(attrs={'class': 'ui dropdown'}),
            'credit': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Credit'}),
            'credit_date': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'reduction': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'reduction_date': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'activate': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'expire': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'deleted': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'registration': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'bill': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
        }


class DvForm(forms.ModelForm):

    class Meta:
        model = Dv
        fields = [
            'user',
            'cid',
            'speed',
            'ip',
            'netmask',
            'logins',
            'filter_id',
            'tp',

        ]

        widgets = {
            'user': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'UID'}),
            'cid': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'speed': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Speed (kb)', 'value': '0'}),
            'ip': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'IP', 'value': '0.0.0.0'}),
            'netmask': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Credit'}),
            'logins': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'filter_id': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Filter ID'}),
            'tp': forms.Select(attrs={'class': 'ui dropdown'}),
        }



class UserPiForm(forms.ModelForm):

    class Meta:
        model = UserPi
        fields = [
            'user_id',
            'fio',
            'email',
            'street',
            'kv',
            'phone',
            'phone2',
            'city',
            'location',
            'contract_date',

        ]

        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'UID'}),
            'fio': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'FIO'}),
            'email': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Mail'}),
            'kv': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Credit'}),
            'phone': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'phone2': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'city': forms.Select(attrs={'class': 'ui dropdown'}),
            'street': forms.Select(attrs={'class': 'ui dropdown'}),
            'location': forms.Select(attrs={'class': 'ui dropdown'}),
            'contract_date': forms.Select(attrs={'class': 'ui dropdown'}),
        }
