from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .decorators import logged_in
from .forms import RegisterForm, LoginForm
from shop.utils import get_cart
from shop.models import Cart
from teach.models import Course
from django.db import IntegrityError

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
            courses = get_cart(request)
            
            course_in_cart = [cart.course.id for cart in Cart.objects.filter(user=user)]
            print(course_in_cart)
            if courses:
                cart_records = [Cart(user=user, course=Course.objects.get(id=course.id)) for course in courses if course.id not in course_in_cart]
                print(cart_records)
                try:
                    Cart.objects.bulk_create(cart_records)
                    del request.session['cart']
                except IntegrityError:
                    del request.session['cart']
                login(request, user)
            else:
                login(request, user)
            
            return redirect('home')
    else:
        form = LoginForm()
        
    return render(request, 'account/login.html', {'form' : form})


def logout_page(request):
    logout(request)
    return redirect('home')