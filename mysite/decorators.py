from django.core.exceptions import PermissionDenied
#from simple_decorators.apps.models import Entry
"""
def user_financ(function):
    def wrap(request, *args, **kwargs):        
        if request.user.has_perm('financ'):
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied
    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
"""