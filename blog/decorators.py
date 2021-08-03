from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    """Decorator to prevent logged in users accessing a page"""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func


def login_needed(view_func):
    """Decorator to prevent a logged out user from accessing a page"""
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('login_page')

    return wrapper_func
