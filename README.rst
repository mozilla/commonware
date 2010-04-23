==========
Commonware
==========

Commonware is a collection of small but useful tools for Django.

They seemed too small to be worth their own packages, but we also wanted
to share them. So here they are.


Logging
=======


commonware.log
--------------

``commonware.log`` overloads ``logging`` to add the IP address of a
request to the log. This is accessed in log formats with ``REMOTE_ADDR``.

To use ``commonware.log``, you need to call ``logging.setLoggerClass()``
before your first call to ``logging.getLogger()``.

For example::

    >>> import logging

    >>> import commonware.log

    >>> logging.setLoggerClass(commonware.log.Logger)

    >>> log = logging.getLogger('z')
    <commonware.log.Logger>

    >>> fmt = '[%(REMOTE_ADDR)s] %(msg)s'

    >>> handler = logging.StreamHandler()
    
    >>> formatter = logging.Formatter(fmt)
    
    >>> handler.setFormatter(formatter)
    
    >>> log.addHandler(handler)


Thread-local storage
^^^^^^^^^^^^^^^^^^^^

``commonware.log`` needs to store the IP address of the request in thread-
local storage. This requires extra middleware to first store the address
before ``commonware.log`` can access it.

Fortunately, that's fairly easy. Just add
``commonware.log.LogRequestThreadMiddleware`` to your ``MIDDLEWARE_CLASSES``
before any other middleware that uses logging.

If a remote IP address can't be found, an empty string will be returned
instead.


Middleware
==========


NoVarySessionMiddleware
-----------------------

By default, Django likes to send ``Vary: Cookie`` if you touch sessions at
all. While that's fine for many users, if your app is behind a load-balancer
or reverse proxy, ``Vary:`` headers can be painful.

``commonware.middleware.NoVarySessionMiddleware`` prevents Django from
adding ``Vary: Cookie``, but protects other ``Vary:`` headers.

To use ``NoVarySessionMiddleware``, replace the Django ``SessionMiddleware``
with ``commonware.middleware.NoVarySessionMiddleware`` in your
``MIDDLEWARE_CLASSES``.


SetRemoteAddrFromForwardedFor
-----------------------------

For servers behind reverse-proxies, either load balancers or caches, the
value of ``request.META['REMOTE_ADDR']`` is usually wrong: it is usually
set to the IP address of the proxy.

``commonware.middleware.SetRemoteAddrFromForwardedFor`` changes the value
of ``request.META['REMOTE_ADDR']`` to the first entry in the
``X-Forwarded-For`` header.

Only use ``SetRemoteAddrFromForwardedFor`` if you know your app is behind
well-behaved reverse proxies, as the ``X-Forwarded-For`` header is very
easy to spoof.
