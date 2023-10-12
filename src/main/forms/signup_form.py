# forms.py
from django import forms

class SignUpForm(forms.Form):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    date_of_birth = forms.DateField()
    # password = forms.CharField(widget=forms.PasswordInput, min_length=2)  # Change min_length to your desired minimum length
    # confirm_password = forms.CharField(widget=forms.PasswordInput, min_length=2)  # Change min_length to your desired minimum length
    
