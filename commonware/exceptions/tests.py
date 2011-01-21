from django.db import DatabaseError

from nose.tools import eq_
from test_utils import RequestFactory

from commonware.exceptions.middleware import HidePasswordOnException


def test_hide_password():
    tests = (
        'password',
        'PASSWORD',
        'password2',
        'confirmpassword',
        'PaSsWorD',
    )

    e = DatabaseError()
    rf = RequestFactory()
    hpoe = HidePasswordOnException()

    def hidden(password):
        post = rf.post('/foo', {password: 'foo'})
        eq_(post.POST[password], 'foo')
        hpoe.process_exception(post, e)
        eq_(post.POST[password], '******')

    for pw in tests:
        yield hidden, pw
