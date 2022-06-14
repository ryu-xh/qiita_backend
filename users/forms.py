from django import forms


class AuthenticationForm(forms.Form):
    handle = forms.CharField(required=True)
    username = forms.CharField(required=False)
    password = forms.CharField(required=True)
