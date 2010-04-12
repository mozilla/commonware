"""
LICENSE GOES HERE
"""

class SetRemoteAddrFromForwardedFor:
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
