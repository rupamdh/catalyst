from .models import Cart
from teach.models import Course

def get_total_cart_price(request):
    carts = Cart.objects.filter(user=request.user)
    total = 0
    if 'buy_now_id' in request.session:
        course = Course.objects.get(id=request.session['buy_now_id'])
        total = course.get_price()
        return total
    else:
        for cart in carts:
            total += cart.course.get_price()
        return total

def get_total_original_price(request):
    carts = Cart.objects.filter(user=request.user)
    total = 0
    if 'buy_now_id' in request.session:
        course = Course.objects.get(id=request.session['buy_now_id'])
        total = course.price
        return total
    else:
        for cart in carts:
            total += cart.course.price
        return total

def get_cart_ids(request):
    carts = Cart.objects.filter(user=request.user)
    cart_ids = []
    cart_ids = [cart.id for cart in carts]
    return cart_ids
