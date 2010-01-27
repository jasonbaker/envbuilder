from setuptools import setup, find_packages

readme = open('README.rst', 'r')

unsplit_readme_text = readme.read()
split_text = [x for x in unsplit_readme_text.split('.. split here')
              if x]
README_TEXT = split_text[-1]
print README_TEXT
readme.close()

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
