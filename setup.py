from setuptools import setup, find_packages

try:
    with open('README.md', 'r') as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ''

setup(
    name='panoptes_aggregation',
    version='1.2.0',
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
            'config_workflow_panoptes=panoptes_aggregation.scripts.config_workflow_panoptes:main',
            'extract_panoptes_csv=panoptes_aggregation.scripts.extract_panoptes_csv:main',
            'reduce_panoptes_csv=panoptes_aggregation.scripts.reduce_panoptes_csv:main'
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
        'scipy',
        'werkzeug'
    ]
)
