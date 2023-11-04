from django.shortcuts import render, redirect
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import SignupForm, LoginForm, ResetPasswordForm, BookAppointmentForm
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from main.models import AppointmentModel

def home(request):
    return render(request, "index.html")

def user_login(request):
    if request.method == 'POST': # django login forms use POST method
        form = LoginForm(request.POST) # send form to server

        if form.is_valid():
            # clean inputs
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(home) # redirect user to home page after user is logged in
            else:
                form = LoginForm()

    return render(request, "login.html")

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
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
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
    
def book_appointment(request):
    # add code to make sure page is not visible unless logged in 
    if request.method == 'POST':
        form = BookAppointmentForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date'] # temporary manual implementation until calander widget or calenar view is implmented
            time = form.cleaned_data['time']
            patient_id = form.cleaned_data['patient_id']

            appointment = AppointmentModel(appointment_date=date, appointment_time=time, patient_id=patient_id)
            appointment.save()
            return redirect('/')
    else:
        form = BookAppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})
