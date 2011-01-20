from functools import wraps

from django.utils.decorators import available_attrs


def xframe_sameorigin(view_fn):
    @wraps(view_fn, assigned=available_attrs(view_fn))
    def _wrapped_view(request, *args, **kwargs):
        response = view_fn(request, *args, **kwargs)
        response['x-frame-options'] = 'SAMEORIGIN'
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
        response['x-frame-options'] = 'DENY'
        return response
    return _wrapped_view


def js_cookies(*cookies):
    def decorator(view_fn):
        @wraps(view_fn, assigned=available_attrs(view_fn))
        def _wrapped_view(request, *args, **kwargs):
            response = view_fn(request, *args, **kwargs)
            response.js_cookies = cookies
            return response
        return _wrapped_view
    return decorator
