import sys
import os

from codecs import open
from os import path
from shutil import rmtree

from setuptools import (
    setup,
    find_packages,
    Command,
)

__version__ = '0.1.0'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [x.strip() for x in all_reqs if 'git+' not in x]
dependency_links = [
    x.strip().replace('git+', '')
    for x
    in all_reqs
    if x.startswith('git+')
]


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.sep.join(('.', 'dist')))
        except FileNotFoundError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(
                sys.executable,
            ),
        )

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name='pytedjmi',
    version=__version__,
    description='Test Django migrations through Pytest.',
    long_description=long_description,
    author='Kit La Touche',
    author_email='kit@transneptune.net',
    url='https://github.com/wlonk/pytest-django-migrations',
    download_url=(
        'https://github.com/wlonk/pytest-django-migrations/tarball/'
        + __version__
    ),
    license='BSD',
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Developers',
      'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    install_requires=install_requires,
    dependency_links=dependency_links,
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)
