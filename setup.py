from setuptools import setup, find_packages

setup(
    name='panoptes_aggregation',
    version='1.0',
    description='Aggegation code for Zooniverse panoptes projects.',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    url='https://github.com/zooniverse/aggregation-for-caesar',
    author='Coleman Krawczyk',
    author_email='coleman@zooniverse.org',
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=[
        'bin/extract_panoptes_csv.py',
        'bin/reduce_panoptes_csv.py',
        'bin/config_workflow_panoptes'
    ],
    packages=find_packages(),
    include_package_data=True,
    extra_require={
        'online': [
            'flask',
            'sphinx',
            'sphinxcontrib-httpdomain'
        ]
    },
    install_requires=[
        'beautifulsoup4',
        'collatex',
        'cython',
        'hdbscan',
        'numpy',
        'pandas',
        'progressbar2',
        'python-levenshtein',
        'python-slugify',
        'pyyaml',
        'scikit-image',
        'scikit-learn',
        'scipy',
        'werkzeug'
    ]
)
