# Using the command line scripts
This package comes with several command line scripts for use with the `csv` data dumps produced by Panoptes.

## Download your data from the project builder
You will need two to three files from your project for offline use:
 - The classification dump: The `Request new classification export` or `Request new workflow classification export` button from the lab's `Data Export` tab
 - The workflow dump: The `Request new workflow export` button from the lab's `Data Export` tab

### Example: Penguin Watch
Penguin Watch has several workflows, for this example we will look at workflow number 6465 (time lapse cameras) and version `52.76`.  The downloaded files for this project are:
 - `penguin-watch-workflows.csv`: the workflow file (contains the major version number as a column)
 - `penguin-watch-classifications-trim.csv`: the classification file for workflow 6465

This [zip folder](https://drive.google.com/file/d/177uXdt3IRIOc2b42UvG4EdNJv973RCtS/view?usp=sharing) contains these files.

---

## Scripts
All scripts are packaged under a single name `panoptes_aggregation`.  Under this command there are three sub-commands `config`, `extract`, and `reduce`.

```bash
usage: panoptes_aggregation [-h] {config,extract,reduce} ...

Aggregate panoptes data files

positional arguments:
  {config,extract,reduce}
    config              Make configuration files for panoptes data extraction
                        and reduction based on a workflow export
    extract             Extract data from panoptes classifications based on
                        the workflow
    reduce              reduce data from panoptes classifications based on the
                        extracted data

optional arguments:
  -h, --help            show this help message and exit
```

## Configure the extractors and reducers
Use the command line tool to make configuration `yaml` files that are used to set up the extractors and reducers.  These base files will use the default settings for various task types. They can be adjusted if the defaults are not needed (e.g. you don't need to extract all the tasks, or you need more control over the reducer's settings).

```bash
usage: panoptes_aggregation config [-h] [-d DIR] [-v VERSION]
                                   [--min_version MIN_VERSION]
                                   [--max_version MAX_VERSION] [-k KEYWORDS]
                                   [-vv]
                                   workflow_csv workflow_id

Make configuration files for panoptes data extraction and reduction based on a
workflow export

optional arguments:
  -h, --help            show this help message and exit

Load Workflow Files:
  This file can be exported from a project\'s Data Export tab

  workflow_csv          The csv file containing the workflow data

Workflow ID and version numbers:
  Enter the workflow ID, major version number, and minor version number

  workflow_id           the workflow ID you would like to extract
  -v VERSION, --version VERSION
                        The workflow version to extract. If only a major
                        version is given (e.g. -v 3) all minor versions will
                        be extracted at once. If a minor version is provided
                        (e.g. -v 3.14) only that specific version will be
                        extracted.
  --min_version MIN_VERSION
                        The minimum workflow version to extract (inclusive).
                        This can be provided as either a major version (e.g.
                        --min_version 3) or a major version with a minor
                        version (e.g. --min_version 3.14). If this flag is
                        provided the --version flag will be ignored.
  --max_version MAX_VERSION
                        The maximum workflow version to extract (inclusive).
                        This can be provided as either a major version (e.g.
                        --max_version 3) or a major version with a minor
                        version (e.g. --max_version 3.14). If this flag is
                        provided the --version flag will be ignored.

Other keywords:
  Additional keywords to be passed into the configuration files

  -k KEYWORDS, --keywords KEYWORDS
                        keywords to be passed into the configuration of a task
                        in the form of a json string, e.g. '{"T0":
                        {"dot_freq": "line"} }' (note: double quotes must be
                        used inside the brackets)

Save Config Files:
  The directory to save the configuration files to

  -d DIR, --dir DIR     The directory to save the configuration files to

Other options:
  -vv, --verbose        increase output verbosity
```

### Example: Penguin Watch
```bash
panoptes_aggregation config penguin-watch-workflows.csv 6465 -v 52.76
```

This creates four files:
 - `Extractor_config_workflow_6465_V52.76.yaml`: The configuration for the extractor code
 - `Reducer_config_workflow_6465_V52.76_point_extractor_by_frame.yaml`: The configuration for the reducer used for the point task
 - `Reducer_config_workflow_6465_V52.76_question_extractor.yaml`: The configuration for the reducer used for the question task
 - `Task_labels_workflow_6465_V52.76.yaml`: A lookup table to translate the column names used in the extractor/reducer output files into the text originally used on the workflow.

---

## Extracting data
Note: this only works for some task types, see the [documentation](https://aggregation-caesar.zooniverse.org/docs) for a full list of supported task types.

Use the command line tool to extract your data into one flat `csv` file for each task type:

```bash
usage: panoptes_aggregation extract [-h] [-d DIR] [-o OUTPUT] [-O]
                                    [-c CPU_COUNT] [-vv]
                                    classification_csv extractor_config

Extract data from panoptes classifications based on the workflow

optional arguments:
  -h, --help            show this help message and exit

Load classification and configuration files:
  classification_csv    The classification csv file containing the panoptes
                        data dump
  extractor_config      The extractor configuration configuration file

What directory and base name should be used for the extractions:
  -d DIR, --dir DIR     The directory to save the extraction file(s) to
  -o OUTPUT, --output OUTPUT
                        The base name for output csv file to store the
                        extractions (one file will be created for each
                        extractor used)

Other options:
  -O, --order           Arrange the data columns in alphabetical order before
                        saving
  -c CPU_COUNT, --cpu_count CPU_COUNT
                        How many cpu cores to use during extraction
  -vv, --verbose        increase output verbosity

```

### Example: Penguin Watch
Before starting let's take a closer look at the extractor configuration file `Extractor_config_workflow_6465_V52.76.yaml`:
```yaml
extractor_config:
    point_extractor_by_frame:
    -   details:
            T0_tool3:
            - question_extractor
        task: T0
        tools:
        - 0
        - 1
        - 2
        - 3
    question_extractor:
    -   task: T6
    -   task: T1
workflow_id: 6465
workflow_version: '52.76'
```
This shows the basic setup for what extractor will be used for each task.  From this configuration we can see that the point extractor will be used for each of the tools in task `T0`, `tool3` of that task will have the question extractor run on its sub-task, and a question extractor will be used for tasks `T1` and `T6`.  If any of these extractions are not desired they can be deleted from this file before running the extractor.  In this case task `T4` was on the original workflow but was never used on the final project, I have already removed it from the configuration above.

Note: If a workflow contains any task types that don't have extractors or reducers they will not show up in this config file.

```bash
panoptes_aggregation extract penguin-watch-classifications-trim.csv Extractor_config_workflow_6465_V52.76.yaml -o example
```

This creates two `csv` files (one for each extractor listed in the config file):
 - `question_extractor_example.csv`
 - `point_extractor_by_frame_example.csv`

---

## Reducing data
Note: this only works for some task types, see the [documentation](https://aggregation-caesar.zooniverse.org/docs) for a full list of supported task types.

```bash
usage: panoptes_aggregation reduce [-h] [-F {first,last,all}] [-O]
                                   [-c CPU_COUNT] [-d DIR] [-o OUTPUT] [-s]
                                   extracted_csv reducer_config

reduce data from panoptes classifications based on the extracted data

optional arguments:
  -h, --help            show this help message and exit

Load extraction and configuration files:
  extracted_csv         The extracted csv file
  reducer_config        The reducer configuration file

What directory and base name should be used for the reductions:
  -d DIR, --dir DIR     The directory to save the reduction file to
  -o OUTPUT, --output OUTPUT
                        The base name for output csv file to store the
                        reductions
  -s, --stream          Stream output to csv after each reduction (this is
                        slower but is resumable)

Reducer options:
  -F {first,last,all}, --filter {first,last,all}
                        How to filter a user making multiple classifications
                        for one subject
  -O, --order           Arrange the data columns in alphabetical order before
                        saving
  -c CPU_COUNT, --cpu_count CPU_COUNT
                        How many cpu cores to use during reduction
```

### Example: Penguin Watch
For this example we will do the point clustering for the task `T0`.  Let's take a look at the default config file for that reducer `Reducer_config_workflow_6465_V52.76_point_extractor_by_frame.yaml`:
```yaml
reducer_config:
    point_reducer_dbscan:
        details:
            T0_tool3:
            - question_reducer
```

As we can see, the default reducer is `point_reducer_dbscan` and the only keyword specified is the only associated with the sub-task of `tool3`.  To get better results we will add some clustering keywords to the configuration of `DBSCAN`:
```yaml
reducer_config:
    point_reducer_dbscan:
        eps: 5
        min_samples: 3
        details:
            T0_tool3:
            - question_reducer
```

But for this project there is a large amount of depth-of-field in the images, leading to a non-constant density of point clusters across the images (more dense in the background of the image and less dense in the foreground).  This means that `HDBSCAN` will work better:
```yaml
reducer_config:
    point_reducer_hdbscan:
        min_cluster_size: 4
        min_samples: 3
        details:
            T0_tool3:
            - question_reducer
```

Now that it is set up we can run:
```bash
panoptes_aggregation reduce point_extractor_by_frame_example.csv Reducer_config_workflow_6465_V52.76_point_extractor_by_frame.yaml -o example
```

This will create one file:
 - `point_reducer_hdbscan_example.csv`: The clustered data points for task `T0`

---

## Reading csv files in python
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
