from django.shortcuts import render, redirect
from .forms import SignupForm

# Create your views here.
def home(request):
    return render(request, "index.html")

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
