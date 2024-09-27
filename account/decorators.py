#custom decorators to redirect logged in user to home page from register page
from django.shortcuts import redirect

def logged_in(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper
