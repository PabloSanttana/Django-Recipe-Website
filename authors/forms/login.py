from django import forms

# fromulario nao atrelado a um model


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label="Username", widget=forms.TextInput(attrs={
        'placeholder': 'Type your username'
    }))
    password = forms.CharField(required=True, label="Password", widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'type': 'password'
    }))
