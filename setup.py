from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='panoptes_aggregation',
    version='2.0.0',
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
            'panoptes_aggregation=panoptes_aggregation.scripts.aggregation_parser:main',
            'panoptes_aggregation_gui=panoptes_aggregation.scripts.gui:gui'
        ]
    },
    packages=find_packages(),
    include_package_data=True,
    extras_require={
        'online': [
            'flask',
        ],
        'doc': [
            'recommonmark',
            'sphinx',
            'sphinxcontrib-httpdomain',
            'sphinx_rtd_theme'
        ],
        'test': [
            'nose',
            'coverage'
        ]
    },
    install_requires=[
        'beautifulsoup4',
        'collatex==2.1.2',
        'Gooey',
        'hdbscan',
        'lxml',
        'numpy>=1.14.5',
        'nose',
        'pandas',
        'progressbar2',
        'python-levenshtein',
        'python-slugify',
        'pyyaml',
        'scikit-image',
        'scikit-learn',
        'scipy>=1.1.0',
        'werkzeug'
    ]
)
