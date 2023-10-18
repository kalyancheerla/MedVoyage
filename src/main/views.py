from django.shortcuts import render
from .forms.login_form import LoginForm
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login


# Create your views here.
def home(request):
    return render(request, "index.html")

# Temporary Signup view. Will be updated later
def signup(request):
    return render(request, "signup.html")

def login(request):
    if request.method == 'POST': # django login forms use POST method
        form = LoginForm(request.POST) # send form to server

        if form.is_valid():
            # clean inputs
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('main/') # redirect user to home page after user is logged in         
    else:
        form = LoginForm()

    return render(request, "login.html")