import os

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))


def path(*args):
    return os.path.join(ROOT, *args)


JINJA_CONFIG = {}

KNOWN_PROXIES = []

SECRET_KEY = 'not so secret key for testing'
