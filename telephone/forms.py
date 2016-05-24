from .models import Client
from django import forms


class ClientAddForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'fio',
            'district',
            'street',
            'house',
            'kv',
            'ur',
        ]
        widgets = {
            'fio': forms.TextInput(attrs={'placeholder': 'FIO', 'class': 'form-control input-sm'}),
            'district': forms.Select(attrs={'placeholder': 'District', 'class': 'form-control input-sm'}),
            'street': forms.Select(attrs={'placeholder': 'Street', 'class': 'form-control input-sm'}),
            'house': forms.Select(attrs={'placeholder': 'House', 'class': 'form-control input-sm'}),
            'kv': forms.TextInput(attrs={'placeholder': 'kv', 'class': 'form-control input-sm'}),
        }


class ClientChangeForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'fio',
            'district',
            'street',
            'house',
            'kv',
            'ur',
        ]
        widgets = {
            'fio': forms.TextInput(attrs={'placeholder': 'FIO', 'class': 'form-control input-sm'}),
            'district': forms.Select(attrs={'placeholder': 'District', 'class': 'form-control input-sm'}),
            'street': forms.Select(attrs={'placeholder': 'Street', 'class': 'form-control input-sm'}),
            'house': forms.Select(attrs={'placeholder': 'House', 'class': 'form-control input-sm'}),
            'kv': forms.TextInput(attrs={'placeholder': 'kv', 'class': 'form-control input-sm'}),
        }