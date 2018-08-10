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

If you see an error about `Cython` not being installed run `pip install cython` and try again.

### With Docker
https://docs.docker.com/get-started/

**Using docker-compose** https://docs.docker.com/compose/
```
docker-compose -f docker-compose.local_scripts.yml build local_scripts
```
From the root directory of this repository, run the desired python scripts using the docker image, e.g. `config_workflow_panoptes --help`
```
docker-compose -f docker-compose.local_scripts.yml run --rm local_scripts config_workflow_panoptes --help

```
**Or directly via docker**
```
docker build . -f Dockerfile.bin_cmds -t aggregation_for_caesar
```
From the root directory of this repository, run the desired python scripts using the docker image, e.g. `config_workflow_panoptes --help`
```
docker run -it --rm --name config_workflow_panoptes -v "$PWD":/usr/src/aggregation aggregation_for_caesar config_workflow_panoptes --help
```

## Download your data from the project builder
You will need two to three files from your project for offline use:
 - The classification dump: The `Request new classification export` or `Request new workflow classification export` button from the lab's `Data Export` tab
 - The workflow dump: The `Request new workflow export` button from the lab's `Data Export` tab
 - The workflow contents (optional): The `Request new workflow contents export` button from the lab's `Data Export` tab.  This file is used to make a look up table between the column names used for each task/answer/tool and the original text used for them on the project.

### Example: Penguin Watch
Penguin Watch has several workflows, for this example we will look at workflow number 6465 (time lapse cameras) and version `57.76`.  The downloaded files for this project are:
 - `penguin-watch-workflows.csv`: the workflow file (contains the major version number as a column)
 - `penguin-watch-workflow_contents.csv`: the workflow contents file (contains the minor version number as a column)
 - `time-lapse-cameras-classifications.csv`: the classification file for workflow 6465


## Configure the extractors and reducers
Use the command line tool to make configuration `yaml` files that are used to set up the extractors and reducers.  These base files will use the default settings for various task types, they can be adjusted if the defaults are not needed (e.g. you don't need to extract all the tasks, or you need more control over the reducer's settings).

```bash
usage: config_workflow_panoptes [-h] [-v VERSION] [-k KEYWORDS]
                                [-c WORKFLOW_CONTENT] [-m MINOR_VERSION]
                                workflow_csv workflow_id

Make configuration files for panoptes data extraction and reduction based on a
workflow export

positional arguments:
  workflow_csv          the csv file containing the workflow data
  workflow_id           the workflow ID you would like to extract

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        The major workflow version to extract
  -k KEYWORDS, --keywords KEYWORDS
                        keywords to be passed into the configuration of a task
                        in the form of a json string, e.g. '{"T0":
                        {"dot_freq": "line"} }' (note: double quotes must be
                        used inside the brackets)
  -c WORKFLOW_CONTENT, --workflow_content WORKFLOW_CONTENT
                        The (optional) workflow content file can be provided
                        to create a lookup table for task/answer/tool numbers
                        to the text used on the workflow.
  -m MINOR_VERSION, --minor_version MINOR_VERSION
                        The minor workflow version used to create the lookup
                        table for the workflow content
```

### Example: Penguin Watch
```bash
config_workflow_panoptes penguin-watch-workflows.csv 6465 -v 52 -c penguin-watch-workflow_contents.csv -m 76
```

This creates four files:
 - `Extractor_config_workflow_6465_V52.yaml`: The configuration for the extractor code
 - `Reducer_config_workflow_6465_V52_point_extractor_by_frame.yaml`: The configuration for the reducer used for the point task
 - `Reducer_config_workflow_6465_V52_question_extractor.yaml`: The configuration for the reducer used for the question task
 - `Task_labels_workflow_6465_V52.76.yaml`: A lookup table to translate the column names used in the extractor/reducer output files into the text originally used on the workflow.

## Extracting data
Note: this only works for some task types, see the [documentation](https://aggregation-caesar.zooniverse.org/docs) for a full list of supported task types.

Use the command line tool to extract your data into one flat `csv` file for each task type:

```bash
usage: extract_panoptes_csv [-h] [-O] [-o OUTPUT]
                            classification_csv extractor_config

extract data from panoptes classifications based on the workflow

positional arguments:
  classification_csv    the classification csv file containing the panoptes
                        data dump
  extractor_config      the extractor configuration yaml file produced by
                        `config_workflow_panoptes`

optional arguments:
  -h, --help            show this help message and exit
  -O, --order           arrange the data columns in alphabetical order before
                        saving
  -o OUTPUT, --output OUTPUT
                        the base name for output csv file to store the
                        annotation extractions (one file will be created for
                        each extractor used)
```

### Example: Penguin Watch
Before starting let's take a closer look at the extractor configuration file `Extractor_config_workflow_6465_V52.yaml`:
```yaml
extractor_config:
  point_extractor_by_frame:
  - details:
      T0_tool3:
      - question_extractor
    task: T0
    tools:
    - 0
    - 1
    - 2
    - 3
  question_extractor:
  - task: T1
workflow_id: 6465
workflow_version: 52
```
This shows the basic setup for what extractor will be used for each task.  From this configuration we can see that the point extractor will be used for each of the tools in task `T0`, `tool3` of that task will have the question extractor run on its sub-task, and a question extractor will be used for tasks `T1`.  If any of these extractions are not desired they can be deleted from this file before running the extractor.  In this case task `T4` was on the original workflow but was never used on the final project, I have already removed it from the configuration above.

Note: If a workflow contains any task types that don't have extractors or reducers they will not show up in this config file.

```bash
extract_panoptes_csv time-lapse-cameras-classifications.csv Extractor_config_workflow_6465_V52.yaml -o example
```

This creates two `csv` files (one for each extractor listed in the config file):
 - `question_extractor_example.csv`
 - `point_extractor_by_frame_example.csv`

## Reducing data
Note: this only works for some task types, see the [documentation](https://aggregation-caesar.zooniverse.org/docs) for a full list of supported task types.

```bash
usage: reduce_panoptes_csv [-h] [-F {first,last,all}] [-O] [-o OUTPUT] [-s]
                           extracted_csv reducer_config

reduce data from panoptes classifications based on the extracted data (see
extract_panoptes_csv)

positional arguments:
  extracted_csv         the extracted csv file output from
                        extract_panoptes_csv
  reducer_config        the reducer yaml file output from
                        config_workflow_panoptes

optional arguments:
  -h, --help            show this help message and exit
  -F {first,last,all}, --filter {first,last,all}
                        how to filter a user making multiple classifications
                        for one subject
  -O, --order           arrange the data columns in alphabetical order before
                        saving
  -o OUTPUT, --output OUTPUT
                        the base name for output csv file to store the
                        reductions
  -s, --stream          stream output to csv after each reduction (this is
                        slower but is resumable)
```

### Example: Penguin Watch
For this example we will do the point clustering for the task `T0`.  Let's take a look at the default config file for that reducer `Reducer_config_workflow_6465_V52_point_extractor_by_frame.yaml`:
```yaml
reducer_config:
  point_reducer_dbscan: {}
```

As we can see, the default reducer is `point_reducer_dbscan` and no keywords have been specified.  To get better results we will add some keywords to the configuration of `DBSCAN`:
```yaml
reducer_config:
  point_reducer_dbscan:
    eps: 5
    min_samples: 3
```

But for this project there is a large amount of depth-of-field in the images, leading to a non-constant density of point clusters across the images (more dense in the background of the image and less dense in the foreground).  This means that `HDBSCAN` will work better:
```yaml
reducer_config:
  point_reducer_hdbscan:
    min_cluster_size: 4
    min_samples: 3
```

Now that it is set up we can run:
```bash
reduce_panoptes_csv point_extractor_by_frame_example.csv Reducer_config_workflow_6465_V52_point_extractor_by_frame.yaml -o example
```

This will create one file:
 - `point_reducer_hdbscan_example.csv`: The clustered data points for task `T0`


## reading csv files in python
The resulting csv files typically contain arrays as values.  These arrays are read in as strings by most csv readers.  To make it easier to read these files in a "science ready" way a utility function for `pandas.read_csv` is provided in `panoptes_aggregation.csv_utils`:
```python
import pandas
from panoptes_aggregation.csv_utils import unjson_dataframe

# the `data.*` columns are read in as strings instead of arrays
data = pandas.read_csv('point_reducer_hdbscan_example.csv')

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
