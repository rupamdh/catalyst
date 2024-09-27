from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .decorators import logged_in
from .forms import RegisterForm, LoginForm


# Create your views here.

@logged_in
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'account/register.html', {'form':form})


@logged_in
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
        
    return render(request, 'account/login.html', {'form' : form})


def logout_page(request):
    logout(request)
    return redirect('home')