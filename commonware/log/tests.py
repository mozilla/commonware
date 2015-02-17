from django.test import SimpleTestCase

import mock
from nose.tools import eq_
from test_utils import RequestFactory

from commonware.log.middleware import (_local, ThreadRequestMiddleware,
                                       get_remote_addr, get_username)


class ThreadRequestMiddlewareTests(SimpleTestCase):
    def setUp(self):
        if hasattr(_local, 'username'):
            delattr(_local, 'username')
        if hasattr(_local, 'remote_addr'):
            delattr(_local, 'remote_addr')
        self.middleware = ThreadRequestMiddleware()

    def test_get_remote_addr(self):
        req = RequestFactory().get('/')
        req.META['REMOTE_ADDR'] = '63.245.217.194'
        eq_(get_remote_addr(), None)
        self.middleware.process_request(req)
        eq_(get_remote_addr(), '63.245.217.194')


    def test_get_username_no_username_field(self):
        req = RequestFactory().get('/')
        req.user = mock.Mock()
        del req.user.USERNAME_FIELD
        req.user.username = 'my-username'
        eq_(get_username(), '<anon>')
        self.middleware.process_request(req)
        eq_(get_username(), 'my-username')


    def test_get_username_with_username_field(self):
        req = RequestFactory().get('/')
        req.user = mock.Mock()
        req.user.USERNAME_FIELD = 'myfield'
        req.user.myfield = 'my-new-username'
        eq_(get_username(), '<anon>')
        self.middleware.process_request(req)
        eq_(get_username(), 'my-new-username')
