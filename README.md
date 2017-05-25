# python-reducers-for-caesar

This is a collection of external reducers written for [caesar](https://github.com/zooniverse/caesar) and offline use.

# Offline use
To install (python 3 only):
```bash
git clone git@github.com:CKrawczyk/python-reducers-for-caesar.git
cd python-reducers-for-caesar
pip install .
```

## Download your data from the project builder
You will need two files for offline use:
 - The classification dump: The `Request new classification export` or `Request new workflow classification export` button from the lab's `Data Export` tab
 - The workflow dump: The `Request new workflow export` button from the lab's `Data Export` tab

## Extracting data
Note: this only works for the drawing tool's point data at the moment
Use the command line tool to extract your data into one flat `csv` file for each extractor used:
```bash
extract_panoptes_csv.py [-h] [-v VERSION] [-o OUTPUT] classification_csv workflow_csv workflow_id

extract data from panoptes classifications based on the workflow

positional arguments:
  classification_csv    the classificaiton csv file containing the panoptes data dump
  workflow_csv          the csv file containing the workflow data
  workflow_id           the workflow ID you would like to extract

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        the workflow version to extract
  -o OUTPUT, --output OUTPUT
                        the output csv file to store the annotation extractions
```

example usage:
```bash
extract_panoptes_csv.py ./classification_dump.csv ./workflow_dump.csv 3513 -v 1 -o ./point_tool_extracts.csv
```
This will extract the user drawn data points from workflow `3513` with a major version of `1`.

# Caesar

## Build/run the app in docker
To run a local version use:
```bash
docker-compose build
docker-compose up
```
and listen on `localhost:5000`.

## run [zappa](https://github.com/Miserlou/Zappa) commands
```bash
docker-compose run aggregation /bin/bash -lc "zappa <cmd>"
```

To deploy to AWS-lambda first update `zappa_settings.json`'s `profile_name` with your `~/.aws/config` profile name and run:
```bash
docker-compose run aggregation /bin/bash -lc "zappa deploy dev"
```
NOTE: the docker container will add your `~/.aws` forlder as a volume.

To update after the first deploy:
```bash
docker-compose run aggregation /bin/bash -lc "zappa update dev"
```

## run tests
To run the tests use:
```bash
docker-compose run aggregation /bin/bash -lc "nosetests -v"
```

## API

### Extractors
Drawn points:
  - endpoint: `extractros/point_extractor`
  - This extracts the data for drawn data points into a form that the `reducers/point_reducer` endpoint can use
  - response contains the original data points into a list for `x` and `y` values of a single classification for each point tool on a workflow.  Example output:
    ```js
    {
      'T0_tool0_x': [
          452.18341064453125,
          190.54489135742188,
          408.8101806640625,
          411.60845947265625,
          482.96441650390625
      ],
      'T0_tool0_y': [
          202.87478637695312,
          306.410888671875,
          235.054931640625,
          158.1024169921875,
          180.4886016845703
      ],
      'T0_tool1_x': [
          404.61279296875,
          422.8015441894531,
          435.3937683105469,
          371.03350830078125
      ],
      'T0_tool1_y': [
          583.4398803710938,
          568.0493774414062,
          612.82177734375,
          617.0191650390625
      ]
    }
    ```

### Reducers
Clustering points:
  - endpoint: `reducers/point_reducer/?eps=5&min_samples=3`
  - This uses [scikitlearn's DBSCAN](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN) to cluster the data points. (NOTE: `eps` is in "pixels")
  - URL args can be set for any of DBSCAN's keywords
  - response contains the original data points, cluster labels, number of clustered points for each label, x and y position (in pixels) of the cluster centers, and values of the covariance matrix for clustered data points for each tool:
    ```js
    {
      T0_tool0_points_x: [1, 2, 3, ...],
      T0_tool0_points_y: [4, 5, 6, ...],
      T0_tool0_cluster_labels: [0, 0, 0, 0, 0, -1, 1, 1, 1, 1, 1, ...],
      T0_tool0_clusters_count: [5, 5, ...],
      T0_tool0_clusters_x: [20, 5, ...],
      T0_tool0_clusters_y: [10, 35, ...],
      T0_tool0_clusters_var_x: [2, 1.5, ...],
      T0_tool0_clusters_var_y: [1.5, 2, ...],
      T0_tool0_clusters_var_x_y: [0.5, -0.5, ...],
      T0_tool1_points...
    }
    ```
