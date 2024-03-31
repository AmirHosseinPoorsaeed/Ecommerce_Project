from functools import wraps
from django.shortcuts import redirect


def unauthenticated_required(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('pages:home')
        else:
            return func(request, *args, **kwargs)

    return wrapper
