from django import forms


class AuthenticationForm(forms.Form):
    handle = forms.CharField(required=True)
    password = forms.CharField(required=True)
