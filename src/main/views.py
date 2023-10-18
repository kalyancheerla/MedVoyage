from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms.signup_form import SignUpForm
from main.models import UserModel
from django.db import IntegrityError



# Create your views here.
def home(request):
    return render(request, "index.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
            except IntegrityError:
                return render(request, 'signup.html', {'form': form, 'error': 'User with the same information already exists.'})
            # Log the user in after successful registration
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})

    return render(request, 'signup.html', {'form': form})

