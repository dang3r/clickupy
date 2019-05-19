import os
from setuptools import setup

# Taken from https://github.com/kennethreitz/setup.py/blob/master/setup.py
here = os.path.abspath(os.path.dirname(__file__))

setup(
    name='clickupy',
    version='0.0.3',
    description='Package for interacting with the clickup api',
    url='https://github.com/dang3r/clickupy',
    author='Daniel Cardoza',
    author_email='dan@danielcardoza.com',
    license='MIT',
    packages=['clickupy'],
    python_requires='>=3.4.0',
    scripts=['bin/clickup'],
    install_requires=['click', 'requests'],
    long_description='\n' + open(os.path.join(here, 'README.md')).read(),
    long_description_content_type='text/markdown',
    zip_safe=False
)
