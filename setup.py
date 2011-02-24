from distutils.core import setup, Command
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'analytical.tests.settings'

cmdclass = {}

try:
    from sphinx.setup_command import BuildDoc
    cmdclass['build_sphinx'] = BuildDoc
except ImportError:
    pass

try:
    from sphinx_pypi_upload import UploadDoc
    cmdclass['upload_sphinx'] = UploadDoc
except ImportError:
    pass


class TestCommand(Command):
    description = "run package tests"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from analytical.tests.utils import run_tests
        run_tests()

cmdclass['test'] = TestCommand


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import analytical

setup(
    name = 'django-analytical',
    version = analytical.__version__,
    license = analytical.__license__,
    description = 'Analytics service integration for Django projects',
    long_description = read('README.rst'),
    author = analytical.__author__,
    author_email = analytical.__email__,
    packages = [
        'analytical',
        'analytical.templatetags',
        'analytical.tests',
        'analytical.tests.templatetags',
    ],
    keywords = ['django', 'analytics'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    platforms = ['any'],
    url = 'http://github.com/jcassee/django-analytical',
    download_url = 'http://github.com/jcassee/django-analytical/archives/master',
    cmdclass = cmdclass,
)
