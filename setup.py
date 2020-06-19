# -*- coding: utf-8 -*-

# DO NOT EDIT THIS FILE!
# This file has been autogenerated by dephell <3
# https://github.com/dephell/dephell

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os.path

readme = ''
here = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(here, 'README.rst')
if os.path.exists(readme_path):
    with open(readme_path, 'rb') as stream:
        readme = stream.read().decode('utf8')

setup(
    long_description=readme,
    name='pytedjmi',
    version='0.4.1',
    description='Test Django migrations through Pytest.',
    python_requires='==3.*,>=3.6.0',
    author='Kit La Touche',
    author_email='kit@transneptune.net',
    classifiers=[
        'Development Status :: 3 - Alpha', 'Framework :: Django',
        'Framework :: Pytest', 'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing'
    ],
    entry_points={'pytest11': ['pytedjmi = pytedjmi.core']},
    packages=['pytedjmi', 'tests.migrations'],
    package_data={},
    install_requires=[
        'django>=3.0.0', 'pytest>=5.4.3',
        'pytest-django>=3.9.0'
    ],
    extras_require={
        'dev': [
            'black==19.10.0', 'coverage', 'flake8', 'isort', 'pytest-cov',
            'sphinx', 'sphinx-rtd-theme', 'tox'
        ]
    },
)
