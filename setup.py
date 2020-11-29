import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc

    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    pass


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import analytical as package  # noqa

setup(
    name='django-analytical',
    version=package.__version__,
    license=package.__license__,
    description=package.__doc__.strip(),
    long_description=read_file('README.rst'),
    long_description_content_type='text/x-rst',
    author=package.__author__,
    author_email=package.__email__,
    packages=[
        'analytical',
        'analytical.templatetags',
        'analytical.tests',
        'analytical.tests.templatetags',
    ],
    keywords=['django', 'analytics'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    platforms=['any'],
    url='https://github.com/jazzband/django-analytical',
    download_url='https://github.com/jazzband/django-analytical/archive/master.zip',
    cmdclass=cmdclass,
)
