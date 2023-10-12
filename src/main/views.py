from django.shortcuts import render
from .forms.login_form import LoginForm

# Create your views here.
def home(request):
    return render(request, "index.html")

# Temporary Signup view. Will be updated later
def signup(request):
    return render(request, "signup.html")

def login(request):
    # if request.method == 'POST': # django login forms use POST method
    #     form = LoginForm(request.POST) # send form to server
    # add code to check if information sent to server is valid

    return render(request, "login.html")