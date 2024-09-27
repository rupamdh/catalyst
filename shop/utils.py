from .models import Cart

def get_total_cart_price(request):
    carts = Cart.objects.filter(user=request.user)
    total = 0
    for cart in carts:
        total += cart.course.get_price()
    return total

def get_total_original_price(request):
    carts = Cart.objects.filter(user=request.user)
    total = 0
    for cart in carts:
        total += cart.course.price
    return total

def get_cart_ids(request):
    carts = Cart.objects.filter(user=request.user)
    cart_ids = []
    cart_ids = [cart.id for cart in carts]
    return cart_ids
