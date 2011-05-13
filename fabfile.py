"""
Creating standalone Django apps is a PITA because you're not in a project, so
you don't have a settings.py file.  I can never remember to define
DJANGO_SETTINGS_MODULE, so I run these commands which get the right env
automatically.
"""
import functools
import os

from fabric.api import local as _local


NAME = os.path.basename(os.path.dirname(__file__))
ROOT = os.path.abspath(os.path.dirname(__file__))

os.environ['DJANGO_SETTINGS_MODULE'] = '%s-project.settings' % NAME
os.environ['PYTHONPATH'] = os.pathsep.join([ROOT,
                                            os.path.join(ROOT, 'examples')])

_local = functools.partial(_local, capture=False)


def shell():
    """Open a Django shell."""
    _local('django-admin.py shell')


def test():
    """Run the tests."""
    _local('nosetests -s')


def coverage():
    """Run the tests with a coverage report."""
    _local('nosetests -s --with-coverage --cover-package=commonware')
