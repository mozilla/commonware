from django.db import DatabaseError

from nose.tools import eq_
from test_utils import RequestFactory

from commonware.exceptions.middleware import ScrubRequestOnException


def test_scrub_request():
    tests = (
        'password',
        'PASSWORD',
        'password2',
        'confirmpassword',
        'PaSsWorD',
    )

    e = DatabaseError()
    rf = RequestFactory()
    hpoe = ScrubRequestOnException()

    def hidden(password):
        sessionid = 'qwertyuiopasdfghjklzxcvbnm'
        rf.cookies['sessionid'] = sessionid
        post = rf.post('/foo', {password: 'foo'})
        eq_(post.POST[password], 'foo')
        eq_(post.COOKIES['sessionid'], sessionid)
        assert sessionid in post.META['HTTP_COOKIE']
        hpoe.process_exception(post, e)
        eq_(post.POST[password], '******')
        eq_(post.COOKIES['sessionid'], '******')
        eq_(post.META['HTTP_COOKIE'], '******')

    for pw in tests:
        yield hidden, pw
