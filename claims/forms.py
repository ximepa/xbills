# # -*- coding: utf-8 -*-
# from django import forms
# from claims.models import User, Claims, Comments, Workers, ClaimState, Priority, Queue
# from django.utils.translation import ugettext_lazy as _
# from django.contrib.auth.forms import UserCreationForm as AuthUserCreationForm, UserChangeForm as AuthUserChangeForm, AuthenticationForm
#
#
# class UserCreationForm(AuthUserCreationForm):
#
#     receive_newsletter = forms.BooleanField(required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'claims_per_page']
#
#     def clean_username(self):
#         username = self.cleaned_data["username"]
#         try:
#             User._default_manager.get(username=username)
#         except User.DoesNotExist:
#             return username
#         raise forms.ValidationError(
#             self.error_messages['duplicate_username'],
#             code='duplicate_username',
#         )
#
#
# class UserChangeForm(AuthUserChangeForm):
#
#     receive_newsletter = forms.BooleanField(required=False)
#
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'claims_per_page']
#
#
# class AboutForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'first_name', 'last_name'
#         ]
#         widgets = {
#             'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Імя',}),
#             'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': u'Фамілія',}),
#         }
#
#
# class SettingsForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = [
#             'claims_per_page'
#         ]
#         widgets = {
#             'claims_per_page': forms.TextInput(attrs={'class': 'form-control'}),
#         }
#
#
# class ClaimsCreateForm(forms.ModelForm):
#     comments = forms.CharField(widget=forms.Textarea, max_length=10000, required=False)
#
#     class Meta:
#         model = Claims
#         fields = [
#             'address', 'uid', 'queue', 'problem', 'state', 'priority', 'worker'
#         ]
#         widgets = {
#             'address': forms.TextInput(attrs={'placeholder': 'Address'}),
#             'uid': forms.TextInput(attrs={'placeholder': 'UID'}),
#             'queue': forms.Select(attrs={'class': 'ui search dropdown'}),
#             'problem': forms.TextInput(attrs={'placeholder': 'Problem'}),
#             'worker': forms.Select(attrs={'class': 'ui search dropdown'}),
#             'state': forms.Select(attrs={'class': 'ui search dropdown'}),
#             'priority': forms.Select(attrs={'class': 'ui search dropdown'}),
#         }
#
#
# class CommentAddForm(forms.ModelForm):
#
#     class Meta:
#         model = Comments
#         fields = [
#             'comments'
#         ]
#         widgets = {
#             'comments': forms.Textarea(attrs={'id': 'id_comm'})
#         }
#
#
# class StateAddForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super(StateAddForm, self).__init__(*args, **kwargs)
#         # access object through self.instance...
#         self.fields['worker'].queryset = Workers.objects.filter(disable=0)
#     worker = forms.ModelChoiceField(required=False, queryset=Workers.objects.all(), empty_label='----------')
#     state = forms.ModelChoiceField(required=True, queryset=ClaimState.objects.all(), empty_label=None)
#     comments = forms.CharField(widget=forms.Textarea(attrs={'id': 'id_comm_state'}), required=False)
#
#
# class PriorityAddForm(forms.Form):
#     priority = forms.ModelChoiceField(required=True, queryset=Priority.objects.all(), empty_label=None)
#     comments = forms.CharField(widget=forms.Textarea(attrs={'id': 'id_comm_prior'}), required=False)
#
# class QueueAddForm(forms.Form):
#     queue = forms.ModelChoiceField(required=True, queryset=Queue.objects.all(), empty_label=None)
#     comments = forms.CharField(widget=forms.Textarea(attrs={'id': 'id_comm_queue'}), required=True)
#
# class CustomAuthenticationForm(AuthenticationForm):
#     # add your form widget here
#     username = forms.CharField(widget=forms.TextInput(attrs={}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
#
#
# class UserSettingsForm(forms.Form):
#     claims_per_page = forms.CharField(required=True)
#     comments_per_page = forms.CharField(required=True)
#     logs_per_page = forms.CharField(required=True)
#     queue = forms.ModelChoiceField(queryset=Queue.objects.all(),widget=forms.Select(), required=True)
#     email = forms.CharField(required=False)