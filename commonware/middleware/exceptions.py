class HidePasswordOnException(object):
    """
    Hide passwords in request.POST so they're not recorded in error logging.
    """

    def process_exception(self, request, exception):
        # Get a copy so it's mutable.
        request.POST = request.POST.copy()
        for key in request.POST:
            if 'password' in key.lower():
                request.POST[key] = '******'
