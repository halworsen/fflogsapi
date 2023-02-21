from setuptools import setup, find_packages
import fflogsapi

setup(
    name='fflogsapi',
    version=fflogsapi.__version__,
    packages=find_packages(include=['fflogsapi*']),
    description='FFLogs API client for Python',
    long_description=open('README.md').read(),
    url='https://github.com/halworsen/fflogsapi',
    author='Markus Wang Halvorsen',
    author_email='mwh@halvorsenfamilien.com',
    license='GPLv3',
    keywords='api client ffxiv fflogs lazy',
    platforms='any',
    install_requires=[
        'gql>=3.4.0',
        'oauthlib>=3.2.2',
        'requests_oauthlib>=1.3.1',
        'requests_toolbelt>=0.10.1',
    ],
)
