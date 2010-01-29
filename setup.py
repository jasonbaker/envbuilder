from setuptools import setup, find_packages

readme = open('README.rst', 'r')

unsplit_readme_text = readme.read()
split_text = [x for x in unsplit_readme_text.split('.. split here')
              if x]
README_TEXT = split_text[-1]
readme.close()

setup(
    name='envbuilder',
    author='Jason Baker',
    author_email='amnorvend@gmail.com',
    version='0.2.0b2',
    packages=find_packages(),
    setup_requires=['nose'],
    install_requires=['ConfigObj>=4.7.0', 'argparse', 'pip', 'virtualenv'],
    zip_safe=False,
    include_package_data=True,
    entry_points = {
        'console_scripts' : [
            'envb = envbuilder.run:main',
            'envbuilder = envbuilder.run:main'            
            ]
        },
    description = "A package for automatic generation of virtualenvs",
    long_description = README_TEXT,
    url='http://github.com/jasonbaker/envbuilder',
    )
