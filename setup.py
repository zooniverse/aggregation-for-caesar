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
            'flask',
            'panoptes-client',
            'pyyaml',
            'requests',
            'gunicorn',
            'sentry-sdk[flask]',
            'newrelic'
        ],
        'doc': [
            'recommonmark',
            'sphinx==2.2.1',
            'sphinxcontrib-httpdomain',
            'sphinx_rtd_theme'
        ],
        'test': [
            'nose',
            'coverage',
            'coveralls',
            'flake8'
        ],
        'gui': [
            'Gooey==1.0.3'
        ]
    },
    install_requires=[
        'beautifulsoup4',
        'collatex==2.2',
        'hdbscan',
        'lxml',
        'numpy==1.17.3',
        'nose',
        'pandas==0.25.3',
        'progressbar2',
        'python-levenshtein',
        'python-slugify',
        'pyyaml',
        'scikit-learn==0.21.3',
        'scipy>=1.1.0',
        'werkzeug'
    ]
)
