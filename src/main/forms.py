from django import forms
from .models import User, Appointments, TestModel, DoctorAppointmentsModel

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    login_type = forms.ChoiceField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('staff', 'Staff')], widget=forms.RadioSelect)
    security_question = forms.CharField()
    class Meta:
        model = User
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

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

class ResetPasswordForm(forms.Form):
    username = forms.CharField()
    security_question = forms.CharField()
    new_password = forms.CharField()

class BookAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('date', 'time', 'details')
    
class UpdatePatientForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email')
    
class CancelAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ('appointment_id',)

class DateInput(forms.DateInput):
    input_type = 'date'

class DoctorAppointments(forms.ModelForm):
    class Meta:
        model = DoctorAppointmentsModel
        fields =('date',)
        widgets = {
            'date': DateInput(),
        }