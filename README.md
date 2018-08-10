# python-reducers-for-caesar

This is a collection of external reducers written for [caesar](https://github.com/zooniverse/caesar) and offline use.

# Documentation
https://aggregation-caesar.zooniverse.org/docs

# Offline use
### With your own python install
To install (python 3 only):
```bash
git clone https://github.com/zooniverse/aggregation-for-caesar.git
cd aggregation-for-caesar
pip install .
```

### With Docker
https://docs.docker.com/get-started/

**Using docker-compose** https://docs.docker.com/compose/
```
docker-compose -f docker-compose.local_scripts.yml build local_scripts
```
From the root directory of this repository, run the desired python scripts using the docker image, e.g. `extract_panoptes_csv.py --help`
```
docker-compose -f docker-compose.local_scripts.yml run --rm local_scripts extract_panoptes_csv --help

```
**Or directly via docker**
```
docker build . -f Dockerfile.bin_cmds -t aggregation_for_caesar
```
From the root directory of this repository, run the desired python scripts using the docker image, e.g. `extract_panoptes_csv.py --help`
```
docker run -it --rm --name extract_panoptes_csv -v "$PWD":/usr/src/aggregation aggregation_for_caesar python bin/extract_panoptes_csv.py --help
```

## Download your data from the project builder
You will need two files for offline use:
 - The classification dump: The `Request new classification export` or `Request new workflow classification export` button from the lab's `Data Export` tab
 - The workflow dump: The `Request new workflow export` button from the lab's `Data Export` tab

## Extracting data
Note: this only works for question tasks and the drawing tool's point data at the moment

Use the command line tool to extract your data into one flat `csv` file for each extractor used:

```bash
usage: extract_panoptes_csv.py [-h] [-v VERSION] [-k KEYWORDS] [-H] [-O]
                               [-o OUTPUT]
                               classification_csv workflow_csv workflow_id

extract data from panoptes classifications based on the workflow

positional arguments:
  classification_csv    the classificaiton csv file containing the panoptes
                        data dump
  workflow_csv          the csv file containing the workflow data
  workflow_id           the workflow ID you would like to extract

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        the workflow version to extract
  -k KEYWORDS, --keywords KEYWORDS
                        keywords to be passed into the extractor for a task in
                        the form of a json string, e.g. '{"T0": {"dot_freq":
                        "line"} }' (note: double quotes must be used inside
                        the brackets)
  -H, --human           switch to make the data column labels use the task and
                        question labels instead of generic labels
  -O, --order           arrange the data columns in alphabetical order before
                        saving
  -o OUTPUT, --output OUTPUT
                        the base name for output csv file to store the
                        annotation extractions (one file will be created for
                        each extractor used)
```

example usage:
```bash
extract_panoptes_csv.py mark-galaxy-centers-and-foreground-stars-classifications.csv galaxy-zoo-3d-workflows.csv 3513 -v 1 -o galaxy_center_and_star_mpl5.csv
```
This will extract the user drawn data points from workflow `3513` with a major version of `1` and place them in a `csv` file named `point_extractor_galaxy_center_and_star_mpl5.csv`.

## Reducing data
Note: this only works for question tasks and the drawing tool's point data at the moment

```bash
usage: reduce_panoptes_csv.py [-h] [-F {first,last,all}] [-k KEYWORDS]
                              [-o OUTPUT]
                              extracted_csv

reduce data from panoptes classifications based on the extracted data (see
extract_panoptes_csv)

positional arguments:
  extracted_csv         the extracted csv file output from
                        extract_panoptes_csv

optional arguments:
  -h, --help            show this help message and exit
  -F {first,last,all}, --filter {first,last,all}
                        how to filter a user makeing multiple classifications
                        for one subject
  -k KEYWORDS, --keywords KEYWORDS
                        keywords to be passed into the reducer in the form of
                        a json string, e.g. '{"eps": 5.5, "min_samples": 3}'
                        (note: double quotes must be used inside the brackets)
  -o OUTPUT, --output OUTPUT
                        the base name for output csv file to store the
                        reductions
  -s, --stream          stream output to csv after each redcution (this is
                        slower but is resumable)
```

example usage:
```bash
reduce_panoptes_csv.py point_extractor_galaxy_center_and_star_mpl5.csv -F first -k '{"eps": 5, "min_sample": 3}' -o 'galaxy_and_star_mpl5.csv'
```
This will produce a reduced `csv` file named `point_reducer_galaxy_and_star_mpl5.csv`.  If a user classified an image more than once only the first one is kept.

## reading csv files in python
The resulting csv files typically contain arrays as values.  These arrays are typically read in as strings by most csv readers.  To make it easier to read these files in a "science ready" way a utility function for `pandas.read_csv` is provided in `panoptes_aggregation.csv_utils`:
```python
import pandas
from panoptes_aggregation.csv_utils import unjson_dataframe

# the `data.*` columns are read in as strings instead of arrays
data = pandas.read_csv('point_reducer_galaxy_and_star_mpl5.csv')

# use unjson_dataframe to convert them to lists
# all values are updated in place leaving null values untouched
unjson_dataframe(data)
```

# Caesar

## Build/run the app in docker
To run a local version use:
```bash
docker-compose build
docker-compose up
```
and listen on `localhost:5000`.  The documentation will automatically be created and added to the '/docs' route.

## run tests
To run the tests use:
```bash
docker-compose run --rm aggregation nosetests
```

# Contributing

1. Use [PEP8](https://www.python.org/dev/peps/pep-0008/) syntax
2. Automatic documentation will be created using [sphinx](http://www.sphinx-doc.org/en/stable/) so add doc strings to any files created and functions written
3. A guide for writing [extractors](panoptes_aggregation/extractors/README.md)
4. A guide for writing [reducers](panoptes_aggregation/reducers/README.md)
