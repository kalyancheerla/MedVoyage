import datetime
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from .utils.twilio_utils import send_sms_verification_code, check_verification_code
from django.conf import settings
from django.http import HttpResponseBadRequest, JsonResponse
from django.forms import formset_factory
from django.utils.dateparse import parse_time
from .forms import SignupForm, LoginForm, ResetPasswordForm, UpdatePatientForm
from .forms import VerificationForm, UpdateDoctorForm, AppointmentForm
from .forms import TimeSlotForm
from .models import DoctorProfile, PatientProfile, Appointments, AvailableSlot

def home(request):
    return render(request, "index.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                request.session['type'] = user.is_doctor
                # Check if the user is verified
                if settings.TWO_FACTOR_AUTH is False or user.is_verified:
                    login(request, user)
                    if user.is_doctor:
                        return redirect('doctor_dashboard')
                    else:
                        return redirect('client_dashboard')
                else:
                    # If the user is not verified, send a verification code to the user's phone number                    
                    phone_number = getattr(user, 'phone')
                    request.session['phone_number'] = phone_number
                    request.session['username'] = username

                    send_sms_verification_code(phone_number)

                    # Redirect to the verification page
                    return redirect('verification')
            else:
                form = LoginForm()

    return render(request, "login.html")

def verification(request):
    if request.method == 'POST':
        form = VerificationForm(request.POST)

        if form.is_valid():
            verification_code = form.cleaned_data['verification']
            phone_number = request.session['phone_number']
            username = request.session['username']
            status = check_verification_code(phone_number, verification_code)
            if status == 'approved':
                # Set the user's verified status to True
                user = get_user_model().objects.get(username=username)
                del request.session['phone_number']
                del request.session['username']
                login(request, user)

                # Redirect to the appropriate dashboard
                type = request.session['type']
                if type:
                    return redirect('doctor_dashboard')
                return redirect('client_dashboard')
            else:
                # If the verification code is invalid, redirect to the verification page and display an error message
                form = VerificationForm()
                return render(request, "verification.html", {'form': form, 'error': 'Invalid verification code'})
        else:
            form = VerificationForm()
            return render(request, "verification.html", {'form': form, 'error': 'Please enter a valid verification code'})

    else:
        form = VerificationForm()

    return render(request, "verification.html", {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            new_password = form.cleaned_data['new_password']
            security_question = form.cleaned_data['security_question']

            user = get_user_model().objects.get(username=username)
            saved_security_question = getattr(user, 'security_question')
            if saved_security_question == security_question:
                user.set_password(new_password)
                user.save()
                return redirect(home)
            else:
                form = ResetPasswordForm()
    return render(request, "reset_password.html")

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_doctor:
                DoctorProfile.objects.create(user=user)
            elif user.is_patient:
                PatientProfile.objects.create(user=user)
            return redirect('/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def about_us(request):
    developers = [
        {'name': 'Kalyan Cheerla', 'bio': 'Project Manager', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Bhavani Rachakatla', 'bio': 'Design and Testing Lead', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Yasmeen Haleem', 'bio': 'Requirements and Documentation Lead', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Demir Altay', 'bio': 'Implementation Lead(backend)', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Vidhi Bhatt', 'bio': 'Implementation Lead(front end)', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Emmie Abels', 'bio': 'Implementation Lead(front end)', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Manushree Buyya', 'bio': 'Demo and Presentation Lead', 'image': 'images/ProfilePic.jpg'},
        {'name': 'Pravallika Bollavaram', 'bio': 'Configuration Management Lead', 'image': 'images/ProfilePic.jpg'},
    ]
    return render(request, "about_us.html", {'developers': developers})

def contact_us(request):
    return render(request,"contact_us.html")

def contact_us_form_submit(request):
    if request.method == 'POST':
        # Need to handle the form submission logic here
        # For now, just redirecting to the same contact us page
        return redirect('contact_us')
    return render(request, 'contact_us.html')

def signout(request):
    logout(request)
    return redirect(home)

def client_dashboard(request):
    return render(request, "clientdashboard.html")

def client_profile(request):
    return render(request, "clientprofile.html")

def update_patient_info(request):
    if request.method == 'POST':
        form = UpdatePatientForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(client_profile)  
    else:
       form = UpdatePatientForm(instance=request.user)
    return render(request, 'clientupdateform.html')
    
def doctor_dashboard(request):
    return render(request, "doctordashboard.html")

def doctor_profile(request):
    return render(request, "doctor_profile.html")

def update_doctor_info(request):
    if request.method == 'POST':
        form = UpdateDoctorForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(doctor_profile)  
    else:
       form = UpdateDoctorForm(instance=request.user)
    return render(request, 'update_doctor_info.html')

def patient_appointments(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest('Missing required field: required_field')
    appointments = Appointments.objects.all()
    past_appointments = []
    upcoming_appointments = []
    for appointment in appointments: 
        if appointment.patient.user.id == request.user.id:
            if appointment.appointment_date >= datetime.date.today():
                upcoming_appointments.append(appointment)
            else:
                past_appointments.append(appointment)
    return render(request, "patient_appointments.html", {'past_appointments': past_appointments, 'upcoming_appointments': upcoming_appointments})

def add_slots(request):
    TimeSlotFormSet = formset_factory(TimeSlotForm, extra=1)
    if request.method == 'POST':
        formset = TimeSlotFormSet(request.POST)
        if formset.is_valid():
            # Iterate over each form in the formset and save the individual forms
            for form in formset.cleaned_data:
                # Only proceed if form has data
                if form:
                    doctor_profile = get_object_or_404(DoctorProfile, user=request.user)
                    new_slot = AvailableSlot(
                        date=form['date'],
                        start_time=form['start_time'],
                        end_time=form['end_time'],
                        doctor=doctor_profile  # Assign the DoctorProfile instance
                    )
                    new_slot.save()
            messages.success(request, "The available slots have been successfully added.")
            return redirect('slots_list')
        else:
            # If the formset is not valid, render the formset back to the page to display errors
            return render(request, 'add_slots.html', {'formset': formset})
    else:
        # If not a POST request, instantiate an empty formset to render on the page
        formset = TimeSlotFormSet()
        return render(request, 'add_slots.html', {'formset': formset})

def success(request):
    return render(request, 'success.html')

@never_cache
def slots_list(request):
    slots = AvailableSlot.objects.filter(doctor__user=request.user).order_by('date', 'start_time')
    no_slots_available = not slots.exists()  # True if no slots are available
    return render(request, 'slots_list.html', {'slots': slots, 'no_slots_available': no_slots_available})

def edit_slot(request, slot_id):
    slot = get_object_or_404(AvailableSlot, id=slot_id)
    if request.method == 'POST':
        form = TimeSlotForm(request.POST, instance=slot)
        if form.is_valid():
            form.save()
            return redirect('slots_list')  # Redirect to the slots list page
    else:
        form = TimeSlotForm(instance=slot)
    return render(request, 'edit_slot.html', {'form': form})

@require_POST
def delete_slot(request, slot_id):
    doctor_profile = get_object_or_404(DoctorProfile, user=request.user)
    slot = get_object_or_404(AvailableSlot, id=slot_id, doctor=doctor_profile)
    slot.delete()
    messages.success(request, "The slot has been successfully deleted.")
    return redirect('slots_list')

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            time_slot = form.cleaned_data['time_slot']
            start_time_str, end_time_str = time_slot.split(' - ')
            appointment = form.save(commit=False)
            # Set the patient to the current user
            appointment.patient = PatientProfile.objects.get(user=request.user)
            appointment.start_time = parse_time(start_time_str)
            appointment.end_time = parse_time(end_time_str)
            appointment.booked_date = datetime.datetime.now()
            appointment.save()
            return redirect('home')  # Redirect to a confirmation or success page
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})

@login_required
def get_doctor_availability_hours(request):
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    time_slots = get_list_or_404(AvailableSlot, doctor_id=doctor_id, date=date)
    time_values = []
    for time_slot in time_slots:
        time_values.append([str(time_slot.start_time), str(time_slot.end_time)])
    return JsonResponse({str(time_slots[0].date): time_values})