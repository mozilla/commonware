from setuptools import setup

setup(
    name='commonware',
    version='0.1.0',
    description='A place to keep stuff we want to share, like middleware.',
    author='James Socol',
    author_email='james@mozilla.com',
    url='http://github.com/jsocol/commonware',
    license='BSD',
    packages=['commonware'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Environment :: Web Environment :: Mozilla',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
