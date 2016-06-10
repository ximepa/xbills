# -*- coding: utf-8 -*-
__author__ = 'ximepa'
from django import forms
from django.forms import ModelForm, Textarea
from core.models import TpGroups
from .models import IptvDevice, IptvDeviceType
from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm, AuthenticationForm



# class UserAddForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('login', 'password', 'email', 'account', 'birth_date', 'gender', 'firstname', 'lastname', 'phone', 'region',
#                   'receive_news', 'send_registration_email', 'index')
#         widgets = {
#             'login': forms.TextInput(attrs={'class': 'form-control input-sm', 'autocomplete': 'off'}),
#             'password': forms.PasswordInput(attrs={'class': 'form-control input-sm'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control input-sm', 'autocomplete': 'off'}),
#             'account': forms.HiddenInput(),
#             'birth_date': forms.DateInput(attrs={'class': 'form-control input-sm', 'data-format': 'yyyy-MM-dd'}),
#         }


# class UserRemoveForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('account',)
#         widgets = {
#             'account': forms.HiddenInput(),
#         }
#
#
# class UserLinkingForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('email', 'account',)
#         widgets = {
#             'email': forms.HiddenInput(),
#             'account': forms.HiddenInput(),
#         }
#
#
# class UserEmailChangeForm(ModelForm):
#     class Meta:
#         model = User
#         fields = ('email', 'account',)
#         widgets = {
#             'email': forms.HiddenInput(),
#             'account': forms.HiddenInput(),
#         }


DEV_CHOICES = (
    ('stb', 'stb'),
    ('dune', 'dune'),
    ('smarttv', 'smarttv'),
    ('lge', 'lge'),
    ('samsung', 'samsung'),
    ('ipad', 'ipad'),
)
DEV_TYPE = (
    ('device_free', 'Новый контракт - 24 мес и оборудование за 1 грн'),
    ('device_buy', 'Новый контракт - покупка оборудования'),
    ('device_rent', 'Новый контракт - аренда оборудования'),
    ('device_change', 'Сервисная замена текущего оборудования'),
)


class DeviceAddForm(ModelForm):
    device_type = forms.ModelChoiceField(queryset=IptvDeviceType.objects.all(), initial=1, widget=forms.Select(attrs={'class': 'form-control'}))
    type = forms.ChoiceField(choices=DEV_TYPE, initial='device_free', widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = IptvDevice
        fields = ('uid', 'device_type', 'mac', 'serial_num', 'model')
        widgets = {
            'account': forms.TextInput(attrs={'class': 'form-control input-sm', 'autocomplete': 'off'}),
            'mac': forms.TextInput(attrs={'class': 'form-control input-sm', 'autocomplete': 'off'}),
            'serial_num': forms.TextInput(attrs={'class': 'form-control input-sm', 'autocomplete': 'off'}),
            'model': forms.TextInput(attrs={'class': 'form-control input-sm', 'autocomplete': 'off'}),
            #'device_type': forms.ModelChoiceField(queryset=IptvDeviceType.objects.all(), ),
        }

    # def __init__(self, *args, **kwargs):
    #     super(DeviceAddForm, self).__init__(*args, **kwargs)
    #     self.fields['device_type'] = forms.ModelChoiceField(queryset=IptvDeviceType.objects.all())


DEV_REMOVE_TYPE = (
    ('device_break_contract', 'Окончание контракта'),
    ('device_change', 'Сервисная проблема оборудования'),
)


class DeviceRemoveForm(forms.Form):
    type = forms.ChoiceField(choices=DEV_REMOVE_TYPE, initial='device_break_contract', widget=forms.Select(attrs={'class': 'form-control'}))


TYPE = (
    ('subs_break_contract', 'Разрыв договора'),
    ('subs_negative_balance', 'Отрицательный баланс'),
    ('subs_malfunction', 'Технические неполадки'),
    ('subs_vacation', 'Каникулы'),
)


class TypeForm(forms.Form):
    type = forms.ChoiceField(choices=TYPE, initial='subs_negative_balance', widget=forms.Select(attrs={'class': 'form-control'}),)


STATUS_FILTER_CHOISES = (
    (None, u'Всі'),
    (0, u'Не активовані'),
    (1, u'Активовані'),
)


class UserFilterForm(forms.Form):
    status = forms.ChoiceField(choices=STATUS_FILTER_CHOISES, initial='0', widget=forms.RadioSelect(attrs={'onclick': 'document.getElementById("filter_form").submit();'}),)
    search = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Search'},))


class UserRegistrationForm(forms.Form):
    email = forms.HiddenInput()
    account = forms.HiddenInput()


class CustomAuthenticationForm(AuthenticationForm):
    # add your form widget here
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логін'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class GroupFilterForm(forms.Form):
    group = forms.ModelChoiceField(queryset=TpGroups.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))