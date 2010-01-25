from setuptools import setup, find_packages

GITHUB_ALERT = """**NOTE**:  These are the docs for the version of envbuilder in git.  For
documentation on the last release, see the `pypi_page <http://pypi.python.org/pypi/envbuilder/>`_."""
readme = open('README.rst', 'r')

README_TEXT = readme.read().replace(GITHUB_ALERT, '')
readme.close()
from nose.tools import set_trace; set_trace()

setup(
    name='envbuilder',
    author='Jason Baker',
    author_email='amnorvend@gmail.com',
    version='0.2.0dev',
    packages=find_packages(),
    setup_requires=['nose'],
    install_requires=['ConfigObj', 'argparse', 'anyjson', 'simplejson'],
    zip_safe=False,
    include_package_data=True,
    entry_points = {
        'console_scripts' : [
            'envb = envbuilder.run:main'
            ]
        },
    description = "A package for automatic generation of virtualenvs",
    long_description = README_TEXT,
    url='http://github.com/jasonbaker/envbuilder',
    )
