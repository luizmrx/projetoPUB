from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):

    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('aacc_app:home')
        
        return view_func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]): # pylint: disable=dangerous-default-value
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
        
            return HttpResponse("Usuário não tem permissão para essa página!")
            
        return wrapper_func
    return decorator
