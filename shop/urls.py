from django.urls import path
from .views import *


urlpatterns = [
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('buy-now/<str:slug>/', buy_now, name='buy_now'),
    path('cart/', cart_page, name='cart'),
    path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
    path('get-side-cart/', get_side_cart, name='get_side_cart'),
    path('checkout/', checkout, name='checkout'),
    path('proceed-checkout/', preoceed_checkout, name='preoceed_checkout'),

    path('success/', order_complete, name='success'),
    path('enrolled-courses/', enrolled_courses, name='enrolled_courses'),
]