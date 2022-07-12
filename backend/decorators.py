from datetime import datetime
from functools import wraps


from graphql.execution.base import ResolveInfo
from django.utils.translation import ugettext as _


from graphql_jwt import exceptions


def context(f):
    def decorator(func):
        def wrapper(*args, **kwargs):
            info = next(arg for arg in args if isinstance(arg, ResolveInfo))
            return func(info.context, *args, **kwargs)
        return wrapper
    return decorator



def user_passes_test(test_func, exc=exceptions.PermissionDenied()):
    def decorator(f):
        @wraps(f)
        @context(f)
        def wrapper(context, *args, **kwargs):
            if test_func(context['user']):
                print(context['user'])
                return f(*args, **kwargs)
            raise exc
        return wrapper
    return decorator


login_required_sub = user_passes_test(lambda u: u.is_authenticated)