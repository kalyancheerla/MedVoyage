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

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField() #needs proper password/auth

class ResetPasswordForm(forms.Form):
    username = forms.CharField()
    security_question = forms.CharField()
    new_password = forms.CharField()

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = PatientModel
        fields = ['first_name', 'last_name', 'phone', 'email']    