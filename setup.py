from setuptools import setup

__version__ = '0.1'
__author__  = 'Leonid Secret'

requirements = 
[
        'beautifulsoup4',
        'requests'
]

description = 'Script for discard.email from console'

setup(
        name='EmConsole_py',
        version=__version__,
        author=__author__,
        author_email='ve8ng@protonmail.com'
        description=description,
        install_requires=requirements
)
