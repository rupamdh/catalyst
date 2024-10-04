from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import stripe.error
from teach.models import Course
from account.models import User
from .models import Cart, Order
from django.db import IntegrityError
from django.template.loader import render_to_string
from .utils import get_total_cart_price, get_total_original_price, get_cart_ids, get_cart
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

import stripe



stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def add_to_cart(request):
    id = request.POST.get('id')
    course = Course.objects.get(id=id)
    if request.user.is_authenticated:
        cart_count = request.user.cart_count()
        try:
            Cart.objects.create(
                user=request.user,
                course=course
            )
            return JsonResponse({'success': True, 'cart_count': int(cart_count + 1)})
        except IntegrityError:
            return JsonResponse({'success': False})
    else:
        if 'cart' in request.session:
            course_in_cart = request.session['cart']
            course_in_cart.append(int(id))
            request.session['cart'] = course_in_cart
        else:
            course_in_cart = []
            course_in_cart.append(int(id))
            request.session['cart'] = course_in_cart
            print(course_in_cart)
        cart_count = Course.objects.filter(id__in=course_in_cart).count()
        return JsonResponse({'success': True, 'cart_count': int(cart_count + 1)})

def cart_page(request):
    total_price = get_total_cart_price(request)
    total_original_price = get_total_original_price(request)
    total_discount = total_original_price - total_price
    courses = get_cart(request)

    context = {
        'courses' : courses,
        'total_price' : total_price,
        'total_original_price' : total_original_price,
        'total_discount' : total_discount
    }
    return render(request, 'shop/cart.html', context)

def remove_from_cart(request):
    id = request.POST.get('id')
    course = Course.objects.get(id=id)
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user, course=course)
        cart.delete()
    else:
        if 'cart' in request.session:
            courses = request.session['cart']
            courses.remove(int(id))
            request.session['cart'] = courses
    return JsonResponse({'success': True})

def get_side_cart(request):
    courses = get_cart(request)
    total_price = get_total_cart_price(request)
    total_item = courses.count()
    html = render_to_string('includes/side_cart.html', {'courses' : courses, 'total_price' : total_price, 'total_item':total_item})
    return JsonResponse({'html' : html, 'total_item':total_item})

def buy_now(request, slug):
    course = Course.objects.get(slug=slug)
    if 'buy_now_id' not in request.session:
        request.session['buy_now_id'] = course.id
    return redirect('checkout')


    

@login_required
def checkout(request):
    carts = Cart.objects.filter(user=request.user)
    total_price = get_total_cart_price(request)
    total_original_price = get_total_original_price(request)
    total_discount = total_original_price - total_price

    context = {
        'carts' : carts,
        'total_price' : total_price,
        'total_original_price' : total_original_price,
        'total_discount' : total_discount

    }
    return render(request, 'shop/checkout.html', context)

@login_required
def preoceed_checkout(request):
    total_price = get_total_cart_price(request)
    cart_ids = get_cart_ids(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        token = data.get('token')
        try:
            charge = stripe.Charge.create(
                amount=total_price*100,
                currency='usd',
                source=token,
                description='Test Charge'
            )
            if charge['status'] == 'succeeded':
                user = request.user
                if 'buy_now_id' in request.session: 
                    Order.objects.create(user=user, course=Course.objects.get(id=request.session['buy_now_id']), payment_method='Card', transaction_id=charge['id'])
                    del request.session['buy_now_id']
                    return redirect('success')
                else:
                    carts = Cart.objects.filter(id__in=cart_ids)
                    order_records = [Order(user=user, course=cart.course, status='CM', payment_method='Card', transaction_id=charge['id']) for cart in carts]
                    Order.objects.bulk_create(order_records)
                    carts.delete()
                    return redirect('success')

            return JsonResponse({'success': True})
        except stripe.error.StripeError as e:
            return JsonResponse({'success': False, 'error' : str(e)})
    else:
        print('Not post')
    return HttpResponse('hello')
        

        
        





def order_complete(request):
    return render(request, 'shop/order_complete.html')

@login_required
def enrolled_courses(request):
    orders = Order.objects.filter(user=request.user)

    context = {
        'orders' : orders
    }
    return render(request, 'shop/enrolled_courses.html', context)

