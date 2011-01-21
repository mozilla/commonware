from django.http import HttpResponse
from mock import patch
from nose.tools import eq_

import commonware.response.cookies.monkeypatch


def test_secure_cookies():
    """Ensure cookies are set as secure and httponly unless exempt."""

    # Not a secure request: Default to httponly=True, secure=False
    with patch.dict('os.environ', {'HTTPS': ''}):
        resp = HttpResponse()
        resp.set_cookie('hello', value='world')
        eq_(resp.cookies['hello'].get('httponly'), True)
        assert not resp.cookies['hello'].get('secure')

    # Secure request => automatically secure cookie, unless exempt.
    with patch.dict('os.environ', {'HTTPS': 'on'}):
        resp = HttpResponse()
        resp.set_cookie('default', value='foo')
        resp.set_cookie('not_secure', value='bar', httponly=False)
        eq_(resp.cookies['default']['secure'], True)
        assert not resp.cookies['not_secure'].get('httponly')
