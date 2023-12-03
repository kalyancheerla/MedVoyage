import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.forms.widgets import DateInput, TimeInput
from . import models

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    login_type = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('staff', 'Staff')], widget=forms.RadioSelect)
    security_question = forms.CharField()
    class Meta:
        model = models.User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'security_question', 'password', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        login_type = self.cleaned_data['login_type']
        user.set_password(self.cleaned_data["password"])
        if login_type == 'doctor':
            user.is_doctor = True
        elif login_type == 'patient':
            user.is_patient = True
        if commit:
            user.save()
        return user

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and not re.match(r'^\+?1?(\d{10}|\d{3}-\d{3}-\d{4})$', phone):
            raise ValidationError("Required phonenumber format: '+15555555555' or '5555555555' or '555-555-5555'")
        return phone

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8 and not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\W).+$', password):
            raise ValidationError("Required Password format: min 8 chars with at least 1 small, capital, number, and special-char each")
        return password

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('Passwords don\'t match.')
        return password2

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField() #needs proper password/auth

class VerificationForm(forms.Form):
    verification = forms.CharField()

class ResetPasswordForm(forms.Form):
    username = forms.CharField()
    security_question = forms.CharField()
    new_password = forms.CharField()

class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'phone', 'email')

class UpdateDoctorForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'phone', 'email')

class TimeSlotForm(forms.ModelForm):
    class Meta: #Tells Django which model should be used to create the form here 'AvailableSlot' and which fields should be included in the form
        model = models.AvailableSlot
        fields = ['date', 'start_time', 'end_time']
        widgets = {
            'date': DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'start_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'end_time': TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        # Check if start_time is earlier than end_time
        if start_time and end_time:
            if end_time <= start_time:
                raise ValidationError(gettext_lazy("End time must be after start time."))

        return cleaned_data

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(
        queryset=models.DoctorProfile.objects.all(),
        label="Doctor",
        to_field_name="id",
        empty_label="Select Doctor",
        widget=forms.Select,
        required=True
    )
    appointment_date = forms.DateField(widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}), required=True)
    time_slot = forms.ChoiceField(choices=[], required=True)

    class Meta:
        model = models.Appointments
        fields = ['appointment_date', 'doctor', 'time_slot', 'details']

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        # Dynamically update the time_slot choices based on selected doctor and date
        if 'doctor' in self.data and 'appointment_date' in self.data:
            try:
                doctor_id = int(self.data.get('doctor'))
                date = self.data.get('appointment_date')
                available_slots = models.AvailableSlot.objects.filter(doctor_id=doctor_id, date=date)
                time_choices = [(f"{slot.start_time.strftime('%H:%M:%S')} - {slot.end_time.strftime('%H:%M:%S')}", f"{slot.start_time.strftime('%H:%M:%S')} - {slot.end_time.strftime('%H:%M:%S')}") for slot in available_slots]
                self.fields['time_slot'].choices = time_choices
            except (ValueError, TypeError):
                self.fields['time_slot'].choices = []
