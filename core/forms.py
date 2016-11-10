# -*- coding: utf-8 -*-
from django.utils.translation import gettext as _
from django import forms
from .models import Admin, District, Street, House, Group, User, Company, Dv, Tp, UserPi, Server
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
            'style',
        ]
        widgets = {
            'login': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'name': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Name'}),
            'disable': forms.CheckboxInput(),
            'theme': forms.Select(attrs={'class': ''}),
            'email': forms.EmailInput(attrs={'class': 'ui small input', 'placeholder': u'Email'}),
            'address': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Address'}),
            'cell_phone': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'phone': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'style': forms.Select(attrs={'class': ''}),
        }


class AdministratorAddForm(forms.ModelForm):
    disable = forms.BooleanField(required=False)

    class Meta:
        model = Admin
        fields = [
            'login',
            'password',
            'name',
            'disable',
            'theme',
            'email',
            'address',
            'cell_phone',
            'phone',
            'style',
        ]
        widgets = {
            'login': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'password': forms.PasswordInput(attrs={'class': 'ui small input', 'placeholder': u'Password'}),
            'name': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Name'}),
            'disable': forms.CheckboxInput(),
            'theme': forms.Select(attrs={'class': ''}),
            'email': forms.EmailInput(attrs={'class': 'ui small input', 'placeholder': u'Email'}),
            'address': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Address'}),
            'cell_phone': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'phone': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'style': forms.Select(attrs={'class': ''}),
        }



class SearchForm(forms.Form):
    DISABLED = (
       ('', _("All")),
       (0, _("Active")),
       (1, _("Disabled")),
       (2, _("Not Active")),
    )
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}))
    uid = forms.CharField(widget=forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'UID'}))
    disabled = forms.ChoiceField(widget=forms.RadioSelect(), choices=DISABLED)
    district = forms.ModelChoiceField(widget=forms.Select(attrs={'class': '', 'placeholder': u'District'}), queryset=District.objects.all(), required=False)
    street = forms.ModelChoiceField(widget=forms.Select(attrs={'class': '', 'placeholder': u'Street'}), queryset=Street.objects.all(), required=False)
    house = forms.ModelChoiceField(widget=forms.Select(attrs={'class': '', 'placeholder': u'House'}), queryset=House.objects.filter(~Q(number="")), required=False,)
    flat = forms.CharField(widget=forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Flat'}))


class SearchFeesForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}))
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'ui search dropdown', 'placeholder': u'District'}), queryset=Group.objects.all(), required=False)


class SearchPaymentsForm(forms.Form):
    login = forms.CharField(widget=forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}))
    group = forms.ModelChoiceField(widget=forms.Select(attrs={'class': 'ui search dropdown', 'placeholder': u'District'}), queryset=Group.objects.all(), required=False)


class ClientForm(forms.ModelForm):
    disable = forms.BooleanField(required=False)
    gid = forms.ModelChoiceField(
        queryset=Group.objects.all(),required=False,
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'ui search dropdown'
            }
        )
    )
    district = forms.ModelChoiceField(required=False,
        queryset=District.objects.all(),
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
            'disable',
            'company',
            'credit',
            'login',
            'credit_date',
            'reduction',
            'reduction_date',
            'activate',
            'expire',
            'deleted',
            'registration',
            # 'bill',
        ]
        widgets = {
            'disable': forms.CheckboxInput(),
            'company': forms.Select(attrs={'class': 'ui search dropdown'}),
            'credit': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Credit'}),
            'login': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'credit_date': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'reduction': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Reduction'}),
            'reduction_date': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'activate': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'expire': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            'deleted': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
            'registration': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'0000-00-00'}),
            # 'bill': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Login'}),
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
    district = forms.ModelChoiceField(
        queryset=District.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'ui search dropdown'
            }
        )
    )

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
            'district',
            'location',
            'contract_date',

        ]

        widgets = {
            'user_id': forms.HiddenInput(),
            'fio': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'FIO'}),
            'email': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Mail'}),
            'kv': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Flat'}),
            'phone': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'phone2': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Phone'}),
            'street': forms.Select(attrs={'class': 'ui dropdown'}),
            'location': forms.Select(attrs={'class': 'ui dropdown'}),
            'contract_date': forms.TextInput(attrs={'class': 'ui small input', 'value': '0000-00-00', 'placeholder': '0000-00-00'}),
        }


class ServerForm(forms.ModelForm):
    disable = forms.BooleanField(required=False)

    class Meta:
        model = Server
        fields = [
            'name',
            'nas_identifier',
            'descr',
            'ip',
            'nas_type',
            'mng_host_port',
            'mng_user',
            'rad_pairs',
            'alive',
            'disable',
            'mac',
        ]

        widgets = {
            'ip': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'IP'}),
            'name': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Name'}),
            'nas_identifier': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'Flat'}),
            'descr': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'descr'}),
            'nas_type': forms.Select(attrs={'class': 'ui dropdown'}),
            'mng_host_port': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'mac'}),
            'mng_user': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'mac'}),
            'mac': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'mac'}),
            'alive': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'mac'}),
            'rad_pairs': forms.TextInput(attrs={'class': 'ui small input', 'placeholder': u'mac'}),
        }
