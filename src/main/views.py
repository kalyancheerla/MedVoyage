from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm, ResetPasswordForm, UpdatePatientForm
from .forms import UpdateDoctorForm
from .models import DoctorProfile, PatientProfile
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from .utils.twilio_utils import send_sms_verification_code
import random
from twilio.rest import Client


def home(request):
    return render(request, "index.html")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            print(user)

            if user is not None:
                # Check if the user is verified
                if user.is_verified:
                    login(request, user)
                    if user.is_doctor:
                        return render(request, 'doctordashboard.html',)
                    else:
                        return render(request, 'clientdashboard.html')
                else:
                    # If the user is not verified, generate and send a verification code
                    print("User is not verified")
                    verification_code = generate_verification_code()
                    
                    phone_number = getattr(user, 'phone')

                    send_sms_verification_code(phone_number, verification_code)

                    # Store the verification code in the session for later validation
                    request.session['verification_code'] = verification_code

                    # Redirect to the verification page
                    return redirect('verification')
            else:
                form = LoginForm()

    return render(request, "login.html")

def generate_verification_code():
    # Generate a random 6-digit verification code
    return str(random.randint(100000, 999999))


def verify_code(request):
    if request.method == 'POST':
        entered_code = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')

        if entered_code == stored_code:
            # Code is valid, mark the user as verified
            request.user.is_verified = True
            request.user.save()

            # Clear the stored verification code from the session
            del request.session['verification_code']

            return redirect('dashboard')  # Redirect to the authenticated user's dashboard
        else:
            # Code is invalid, handle accordingly (e.g., display an error message)
            pass

    return render(request, 'verify_code.html')

def verification(request):
    return render(request, "verification.html")


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