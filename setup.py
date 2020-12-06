import os

from setuptools import setup

import analytical as package


def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


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
    ],
    keywords=[
        'django',
        'analytics',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
        'Framework :: Django :: 3.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    platforms=['any'],
    url='https://github.com/jazzband/django-analytical',
    download_url='https://github.com/jazzband/django-analytical/archive/master.zip',
    project_urls={
        'Documentation': 'https://django-analytical.readthedocs.io/',
    },
)
