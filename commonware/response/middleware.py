from django.conf import settings


class FrameOptionsHeader(object):
    """
    Set an X-Frame-Options header. Default to DENY. Set
    response['x-frame-options'] = 'SAMEORIGIN'
    to override.
    """

    def process_response(self, request, response):
        if hasattr(response, 'no_frame_options'):
            return response

        if not 'x-frame-options' in response:
            response['x-frame-options'] = 'DENY'

        return response


class StrictTransportMiddleware(object):
    """
    Set the Strict-Transport-Security header on responses. Use the
    STS_MAX_AGE setting to control the max-age value.
    (Default: 1 month.)
    """

    def process_response(self, request, response):
        age = getattr(settings, 'STS_MAX_AGE', 2592000)  # 30 days.
        response['Strict-Transport-Security'] = 'max-age=%d' % age
        return response
