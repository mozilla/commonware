from django.http import HttpResponse
from mock import patch

from commonware.response.cookies.monkeypatch import patch_all


patch_all()


def test_insecure_response_cookies():
    """Ensure cookies are set as secure and httponly unless exempt."""

    # Not a secure request: Default to httponly=True, secure=False
    with patch.dict('os.environ', {'HTTPS': ''}):
        resp = HttpResponse()
        resp.set_cookie('hello', value='world')
        assert resp.cookies['hello']['httponly']
        assert not resp.cookies['hello']['secure']


def test_secure_response_cookies():

    # Secure request => automatically secure cookie, unless exempt.
    with patch.dict('os.environ', {'HTTPS': 'on'}):
        resp = HttpResponse()
        resp.set_cookie('default', value='foo')
        resp.set_cookie('not_secure', value='bar', secure=False)
        assert resp.cookies['default']['secure']
        assert not resp.cookies['not_secure']['secure']


def test_no_httponly_cookies():
    resp = HttpResponse()
    resp.set_cookie('default', value='foo')
    resp.set_cookie('js_ok', value='bar', httponly=False)
    assert resp.cookies['default']['httponly']
    assert not resp.cookies['js_ok']['httponly']
