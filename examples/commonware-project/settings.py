import os

# Make filepaths relative to settings.
ROOT = os.path.dirname(os.path.abspath(__file__))
path = lambda *a: os.path.join(ROOT, *a)

JINJA_CONFIG = {}

SECURE_HSTS_INCLUDE_SUBDOMAINS = False

KNOWN_PROXIES = []

SECRET_KEY = 'not so secret key for testing'
