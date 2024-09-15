from django import forms

class RegisterForm(forms.Form):
    username=forms.CharField(max_length=120)
    email=forms.EmailField()
    password=forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username_or_email=forms.CharField(max_length=120)
    password=forms.CharField(widget=forms.PasswordInput)