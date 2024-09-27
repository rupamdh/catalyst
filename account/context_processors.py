from .models import *

def user_data(request):
    if request.user.is_authenticated:
        user = request.user
        full_name = f'{user.first_name} {user.last_name}'


        return {
            'user' : user,
            'full_name' : full_name
        }
    else:
        return {}