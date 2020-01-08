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
            'flask>=1.0,<1.2',
            'panoptes-client>=1.1,<1.2',
            'requests>=2.4.2,<2.23',
            'gunicorn>=20.0,<20.1',
            'sentry-sdk[flask]>=0.13.5,<0.14',
            'newrelic>=5.4.0,<5.4.2'
        ],
        'doc': [
            'recommonmark>=0.5.0,<0.7',
            'sphinx>=2.2.2,<2.4',
            'sphinxcontrib-httpdomain>=1.7.0,<1.8',
            'sphinx_rtd_theme>=0.4.3,<0.5'
        ],
        'test': [
            'nose>=1.3.7,<1.4',
            'coverage>=4.5.3,<5.1',
            'coveralls>=1.8,<1.10.1',
            'flake8>=3.7,<3.8',
            'flake8-black>=0.1.1,<0.2',
            'flake8-bugbear>=20.1.2,<20.2'
        ],
        'gui': [
            'Gooey>=1.0.3,<1.1'
        ]
    },
    install_requires=[
        'beautifulsoup4>=4.8.1,<4.9',
        'collatex>=2.2,<2.3',
        'hdbscan>=0.8.20,<0.8.25',
        'lxml>=4.4,<4.5',
        'numpy>=1.16.3,<1.19',
        'pandas>=0.24.2,<0.25.4',
        'progressbar2>=3.39,<3.48',
        'python-levenshtein>=0.12.0,<0.13',
        'python-slugify>=3.0.0,<4.1',
        'pyyaml>=5.1,<5.4',
        'scikit-learn>=0.21.1,<0.22.2',
        'scipy>=1.2,<1.4.2',
        'werkzeug>=0.14,<0.16.1'
    ]
)
