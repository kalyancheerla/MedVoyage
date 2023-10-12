from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms.signup_form import SignUpForm

# Create your views here.
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            date_of_birth = form.cleaned_data['date_of_birth']
            # password = form.cleaned_data['password']
            # confirm_password = form.cleaned_data['confirm_password']
            # if password != confirm_password:
            #     return render(request, 'signup.html', {'form': form, 'error': 'Passwords do not match.'})

            print(username, email, first_name, last_name, date_of_birth)

            # user = User.objects.create_user(username=username, email=email, password=password)
            # user = authenticate(username=username, password=password)
            # if user:
            #     login(request, user)

            return redirect('/')
        else:
            # Form is not valid; render the form with validation errors
            return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

