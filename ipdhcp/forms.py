from django.utils.translation import gettext as _
from django import forms
from .models import Dhcphosts_hosts, Dhcphosts_networks
from core.validators import validate_mac


class Dhcphosts_hostsForm(forms.ModelForm):
    disable = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                'onclick': 'ipdhcp_disable'
            }
        ),
        required=False,
    )
    mac = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control', 'placeholder': u'Mac'
            }
        ),
        validators=[validate_mac]
    )
    network = forms.ModelChoiceField(
        queryset=Dhcphosts_networks.objects.all(),
        empty_label=None,
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Dhcphosts_hosts
        fields = [
            'uid',
            'ip',
            'hostname',
            'network',
            'mac',
            'disable',
            'vid',
            'server_vid',
        ]
        widgets = {
            'uid': forms.HiddenInput(),
            'ip': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Ip', 'aria-describedby': 'select_input', 'id': 'id_ip'}),
            'hostname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Hostname'}),
            'vid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Client vid'}),
            'server_vid': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Server vid'}),
        }