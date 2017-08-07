from setuptools import setup, find_packages

setup(
    name='panoptes_aggregation',
    version='0.1',
    description='Aggegation code for Zooniverse panoptes projects.',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    url='https://github.com/zooniverse/aggregation-for-caesar',
    author='Coleman Krawczyk',
    author_email='coleman@zooniverse.org',
    test_suite='nose.collector',
    tests_require=['nose'],
    scripts=['bin/extract_panoptes_csv.py', 'bin/reduce_panoptes_csv.py'],
    packages=find_packages(),
    include_package_data=True,
    extra_require={
        'online': [
            'flask',
            'sphinx',
            'sphinxcontrib-httpdomain',
            'numpydoc'
        ]
    },
    install_requires=[
        'numpy',
        'pandas',
        'progressbar2',
        'python-slugify',
        'scikit-image',
        'scikit-learn',
        'scipy',
        'slugify',
        'werkzeug'
    ]
)
