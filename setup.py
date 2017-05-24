from setuptools import setup, find_packages

setup(name='panoptes_aggregation',
           version='0.1',
           description='Aggegation code for Zooniverse panoptes projects.',
           classifiers=['Programming Language :: Python :: 3 :: Only'],
           url='https://github.com/CKrawczyk/python-reducers-for-caesar',
           author='Coleman Krawczyk',
           author_email='coleman@zooniverse.org',
           test_suite='nose.collector',
           tests_require=['nose'],
           scripts=['bin/extract_panoptes_csv.py'],
           packages=find_packages(),
           include_package_data=True,
           install_requires=[
               'numpy',
               'pandas',
               'progressbar2',
               'scikit-image',
               'scikit-learn',
               'scipy'
           ])
