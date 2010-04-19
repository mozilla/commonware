from django.contrib.sessions.middleware import SessionMiddleware


class NoVarySessionMiddleware(SessionMiddleware):
    """
    SessionMiddleware sets Vary: Cookie anytime request.session is accessed.
    request.session is accessed indirectly anytime request.user is touched.
    We always touch request.user to see if the user is authenticated, so every
    request would be sending vary, so we'd get no caching.

    We skip the cache in Zeus if someone has a session cookie, so varying on
    Cookie at this level only hurts us.
    """

    def process_response(self, request, response):
        # Let SessionMiddleware do its processing but prevent it from changing
        # the Vary header.
        vary = response.get('Vary', None)
        new_response = (super(NoVarySessionMiddleware, self)
                        .process_response(request, response))
        if vary:
            new_response['Vary'] = vary
        else:
            del new_response['Vary']
        return new_response


class SetRemoteAddrFromForwardedFor(object):
    """
    Replaces the Django 1.1 middleware to replace the remote IP with
    the value of the X-Forwarded-For header for use behind reverse proxy
    servers, like load balancers.
    """

    def process_request(self, request):
        try:
            real_ip = request.META['HTTP_X_FORWARDED_FOR']
        except KeyError:
            return None

        real_ip = real_ip.split(',')[0].strip()
        request.META['REMOTE_ADDR'] = real_ip
