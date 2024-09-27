from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
import stripe.error
from teach.models import Course
from account.models import User
from .models import Cart, Order
from django.db import IntegrityError
from django.template.loader import render_to_string
from .utils import get_total_cart_price, get_total_original_price, get_cart_ids
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import stripe



stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
def add_to_cart(request):
    id = request.POST.get('id')
    course = Course.objects.get(id=id)
    cart_count = request.user.cart_count()

    try:
        Cart.objects.create(
            user=request.user,
            course=course
        )
        return JsonResponse({'success': True, 'cart_count': int(cart_count + 1)})
    except IntegrityError:
        return JsonResponse({'success': False})

def cart_page(request):
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
    return render(request, 'shop/cart.html', context)

def remove_from_cart(request):
    id = request.POST.get('id')
    cart = Cart.objects.get(id=id)
    cart.delete()
    return JsonResponse({'success': True})

def get_side_cart(request):
    carts = Cart.objects.filter(user=request.user)
    total_price = get_total_cart_price(request)
    total_item = carts.count()
    html = render_to_string('includes/side_cart.html', {'carts' : carts, 'total_price' : total_price, 'total_item':total_item})
    return JsonResponse({'html' : html, 'total_item':total_item})

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

def preoceed_checkout(request):
    total_price = get_total_cart_price(request)
    cart_ids = get_cart_ids(request) 

    if request.method == 'POST':
        payment_method = request.POST['payment_method']

        ##Process Stripe Payment Method
        if payment_method == 'stripe':
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data' : {
                            'currency' : 'usd',
                            'unit_amount' : total_price * 100,
                            'product_data' :{
                                'name' : 'Catalyst Course',
                                'description' : 'Buy course'
                            }
                        },
                        'quantity' : 1
                    }
                ],
                metadata = {
                    'cart_ids': ','.join(map(str, cart_ids)),
                    'user_id': request.user.id,
                },
                mode='payment',
                success_url = request.build_absolute_uri('/success/'),
                cancel_url = request.build_absolute_uri('/')
            )
            return redirect(checkout_session.url)



@csrf_exempt
def payment_confirmation(request):
    payload = request.body
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event["data"]["object"]
        cart_ids = session['metadata']['cart_ids'].split(',')
        user_id = session['metadata']['user_id']
        user = User.objects.get(id=user_id)
        carts = Cart.objects.filter(id__in=cart_ids)
        order_records = [Order(user=user, course=cart.course, status='CM') for cart in carts]
        print(order_records)
        Order.objects.bulk_create(order_records)
        carts.delete()
    return HttpResponse(status=200)


def order_complete(request):
    return render(request, 'shop/order_complete.html')