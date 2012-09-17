from functools import wraps

from django.utils.decorators import available_attrs


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
