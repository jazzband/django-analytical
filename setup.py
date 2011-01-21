from distutils.core import setup, Command

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
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        os.environ['DJANGO_SETTINGS_MODULE'] = 'analytical.tests.settings'
        from analytical.tests.utils import run_tests
        run_tests()

cmdclass['test'] = TestCommand


import analytical

setup(
    name = 'django-analytical',
    version = analytical.__version__,
    license = analytical.__license__,
    description = 'Analytics services for Django projects',
    long_description = analytical.__doc__,
    author = analytical.__author__,
    author_email = analytical.__email__,
    packages = [
        'analytical',
        'analytical.templatetags',
        'analytical.tests',
    ],
    keywords = ['django', 'analytics]'],
    classifiers = [
        'Development Status :: 5 - Production/Stable',
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
