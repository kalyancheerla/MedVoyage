from django import forms
from .models import PatientModel

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    login_type = forms.ChoiceField(choices=PatientModel.LOGIN_CHOICES, widget=forms.RadioSelect, initial='both')
    security_question = forms.CharField()
    class Meta:
        model = PatientModel
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'security_question', 'password')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField() #needs proper password/auth

class ResetPasswordForm(forms.Form):
    username = forms.CharField()
    security_question = forms.CharField()
    new_password = forms.CharField()

