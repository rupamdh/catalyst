from django import template
register = template.Library()
from teach.models import Course

@register.filter(name='get_offer')
def get_offer(id):
    course = Course.objects.get(id=id)
    price = course.price
    off_price = course.off_price
    if price and off_price:
        percent = 0
        percent = ((price - off_price) / price) * 100 if off_price > 0 else 0
        return round(percent) if percent > 0 else None
    else: 
        return None



# def fundamental_of_life(you):
#     if you.gender == 'Male':
#         you.earn_money()
#     return you.love

# def fundamental_of_life_v2(you):
#     if you in ['Women', 'Children', 'Dog']:
#         return you.get('Love')
#     elif you.provide('Something'):
#         return you.get('Love')
    

