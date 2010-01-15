from setuptools import setup, find_packages

readme = open('README.rst', 'r')
README_TEXT = readme.read()
readme.close()

setup(
    name='envbuilder',
    author='Jason Baker',
    author_email='amnorvend@gmail.com',
    version='0.1.3',
    packages=find_packages(),
    setup_requires=['nose'],
    install_requires=['ConfigObj', 'argparse'],
    zip_safe=False,
    include_package_data=True,
    entry_points = {
        'console_scripts' : [
            'envbuilder = envbuilder.run:main'
            ]
        },
    description = "A package for automatic generation of virtualenvs",
    long_description = README_TEXT,
    url='http://github.com/jasonbaker/envbuilder',
    )
