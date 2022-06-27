from setuptools import setup, find_packages
import re
import os

here = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(here, 'README.md'), 'r') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ''

try:
    with open(os.path.join(here, 'panoptes_aggregation/version/__init__.py'), 'r') as fp:
        version_file = fp.read()
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]",
        version_file,
        re.M
    )
    if version_match:
        VERSION = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string.")
except FileNotFoundError:
    VERSION = '0.0.0'


setup(
    name='panoptes_aggregation',
    python_requires='>=3',
    version=VERSION,
    description='Aggregation code for Zooniverse panoptes projects.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache License 2.0',
    classifiers=[
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: Apache Software License'
    ],
    url='https://github.com/zooniverse/aggregation-for-caesar',
    author='Coleman Krawczyk',
    author_email='coleman@zooniverse.org',
    test_suite='nose.collector',
    tests_require=['nose'],
    entry_points={
        'console_scripts': [
            'panoptes_aggregation = panoptes_aggregation.scripts.aggregation_parser:main'
        ],
        'gui_scripts': [
            'panoptes_aggregation_gui = panoptes_aggregation.scripts.gui:gui'
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    extras_require={
        'online': [
            'flask>=1.0,<2.2',
            'flask-cors>=3.0,<3.1',
            'panoptes-client>=1.1,<1.6',
            'requests>=2.4.2,<2.29',
            'gunicorn>=20.0,<20.2',
            'sentry-sdk[flask]>=0.13.5,<1.7',
            'newrelic>=5.4.0,<7.12.1',
            'gitpython>=3.0.0,<3.2'
        ],
        'doc': [
            'matplotlib>=3.5.1,<3.6',
            'myst-nb>=0.13.2,<0.17',
            'sphinx>=2.2.2,<5.1',
            'sphinxcontrib-httpdomain>=1.7.0,<1.9',
            'sphinx_rtd_theme>=0.4.3,<1.1'
        ],
        'test': [
            'nose>=1.3.7,<1.4',
            'coverage>=4.5.3,<6.5',
            'coveralls>=3.0.0,<3.3.2',
            'flake8>=3.7,<4.1',
            'flake8-black>=0.1.1,<0.4',
            'flake8-bugbear>=20.1.2,<22.7'
        ],
        'gui': [
            'Gooey>=1.0.3,<1.1'
        ]
    },
    install_requires=[
        'beautifulsoup4>=4.8.1,<4.11',
        'collatex>=2.2,<2.3',
        'hdbscan>=0.8.20,<0.8.29',
        'lxml>=4.4,<4.10',
        'numpy>=1.21.5,<1.23.1',
        'packaging>=20.1,<21.4',
        'pandas>=1.0.0,<1.4.4',
        'progressbar2>=3.39,<4.1',
        'python-levenshtein>=0.12.0,<0.13',
        'python-slugify>=3.0.0,<6.2',
        'pyyaml>=5.1,<6.1',
        'scikit-learn>=1.0.0,<1.1.2',
        'scipy>=1.2,<1.8.2',
        'werkzeug>=0.14,<2.1.3',
        'shapely>=1.7.1,<1.8.3',
    ]
)
