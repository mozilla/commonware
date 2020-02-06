from functools import WRAPPER_ASSIGNMENTS, wraps


# Taken from from django.utils.decorators.available_attrs
def available_attrs(fn):
    """
    Return the list of functools-wrappable attributes on a callable.
    This was required as a workaround for http://bugs.python.org/issue3445
    under Python 2.
    """
    return WRAPPER_ASSIGNMENTS


def xframe_sameorigin(view_fn):
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        response = view_fn(request, *args, **kwargs)
        response['X-Frame-Options'] = 'SAMEORIGIN'
        return response
    return _wrapped_view


def xframe_allow(view_fn):
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        response = view_fn(request, *args, **kwargs)
        response.no_frame_options = True
        return response
    return _wrapped_view


def xframe_deny(view_fn):
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        response = view_fn(request, *args, **kwargs)
        response['X-Frame-Options'] = 'DENY'
        return response
    return _wrapped_view


def xrobots_exempt(view_fn):
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        response = view_fn(request, *args, **kwargs)
        response.no_robots_tag = True
        return response
    return _wrapped_view


def xrobots_tag(rule='noindex'):
    def decorator(view_fn):
        @wraps(view_fn, assigned=available_attrs(view_fn))
        def _wrapped_view(request, *args, **kwargs):
            response = view_fn(request, *args, **kwargs)
            response['X-Robots-Tag'] = rule
            return response
        return _wrapped_view
    return decorator
