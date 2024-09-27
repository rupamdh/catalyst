from .models import *

def shop_data(request):
    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user)
        total_price = 0
        for cart in carts:
            total_price += cart.course.get_price()
        

        return {
            'total_price' : total_price  
        }
    else:
        return {
            
        }