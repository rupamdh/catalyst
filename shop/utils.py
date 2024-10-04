from .models import Cart
from teach.models import Course

def get_cart(request):
    courses_in_cart = []
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        courses_in_cart = [cart.course.id for cart in carts]
    else:
        if 'cart' in request.session:
            courses_in_cart = request.session['cart']
    cart_courses = Course.objects.filter(id__in=courses_in_cart)
    return cart_courses


def get_total_cart_price(request):
    courses = get_cart(request)
    total = 0
    for course in courses:
        total += course.get_price()
    return total

def get_total_original_price(request):
    courses = get_cart(request)
    total = 0
    for course in courses:
        total += course.price
    return total

def get_cart_ids(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        cart_ids = []
        cart_ids = [cart.id for cart in carts]
        return cart_ids
    else:
        return 0