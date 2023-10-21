from django import forms
from .models import PatientModel

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    login_type = forms.ChoiceField(choices=PatientModel.LOGIN_CHOICES, widget=forms.RadioSelect, initial='both')

    class Meta:
        model = PatientModel
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']