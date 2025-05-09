[![DOI](https://zenodo.org/badge/98517215.svg)](https://zenodo.org/badge/latestdoi/98517215)
[![Coverage Status](https://coveralls.io/repos/github/zooniverse/aggregation-for-caesar/badge.svg?branch=master)](https://coveralls.io/github/zooniverse/aggregation-for-caesar?branch=master)

# Getting started

This is a collection of external reducers written for [caesar](https://github.com/zooniverse/caesar) and offline use.

---

## Documentation
You can find the [latest documentation](https://aggregation-caesar.zooniverse.org/docs) on the aggregations code's website.

---

## Download and run
You can find the latest standalone application version to download under 'Assets' on the [Github releases page](https://github.com/zooniverse/aggregation-for-caesar/releases). There are different `.zip` files for Windows/MacOS(Intel)/MacOS(ARM), choose the correct file for you operating system.

Once downloaded, unzip and double click to run.

```{warning}
As this program is unsigned, there will be a warning on both Windows and on MacOS. On Windows click 'run anyway' and on MacOS allow the program in your security settings.
```

This is a standalone version that does not need a local installation of [Python](https://www.python.org/downloads/) or [any dependancies](https://github.com/zooniverse/aggregation-for-caesar/blob/master/pyproject.toml).

---

## Manual installing for offline use
### With your own python install (python 3.9 or higher only)
Install the latest stable release:
```bash
pip install panoptes_aggregation
```

Upgrade and existing installation:
```bash
pip install -U panoptes_aggregation
```

Or for development or testing, you can install the latest development version directly from GitHub:
```bash
pip install -U git+https://github.com/zooniverse/aggregation-for-caesar.git
```

#### Install the Graphical User Interface (GUI)
If you would like to use the GUI instead of the command line install the package with:
```bash
pip install "panoptes_aggregation[gui]"
```

Or for the latest development build from GitHub:
```bash
pip install -U git+https://github.com/zooniverse/aggregation-for-caesar.git#egg=panoptes-aggregation[gui]
```

On linux systems you may need to install GTK3:
```bash
sudo apt-get install build-essential libgtk-3-dev
```

#### Mac Anaconda build
If you are installing this code on a Mac using the anaconda build of python and you want to use the GUI instead of the command line you will have to update one line of the of code in the `panoptes_aggregation_gui` script.  Change the first line from:
```python
#!/path/to/anaconda/python/bin/python
```
to:
```python
#!/bin/bash /path/to/anaconda/python/bin/python.app
```

You can find the location of this file with the command:
```bash
which panoptes_aggregation_gui
```

You will also need to run:
```bash
conda install python.app
```

### With Docker
[https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)

**Using docker-compose** [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
```
docker compose -f docker-compose.local_scripts.yml build local_scripts
```
From the root directory of this repository, run the desired python scripts using the docker image, e.g. `config_workflow_panoptes --help`
```
docker compose -f docker-compose.local_scripts.yml run --rm local_scripts panoptes_aggregation --help
```

**Or directly via docker**
```
docker build . -f Dockerfile.bin_cmds -t aggregation_for_caesar
```
From the root directory of this repository, run the desired python scripts using the docker image, e.g. `panoptes_aggregation --help`
```
docker run -it --rm --name config_workflow_panoptes -v "$PWD":/usr/src/aggregation aggregation_for_caesar panoptes_aggregation --help
```

**Note** The GUI does not work inside a docker container.

---

## Installing for online use
The docker file included is ready to be deployed on any server.  Once deployed, the extractors will be available on the `/extractors/<name of extractor function>` routes and the reducers will be available on the `/reducers/<name of reducer function>` routes.  Any keywords passed into these functions should be included as url parameters on the route (e.g. `https://aggregation-caesar.zooniverse.org/extractors/point_extractor_by_frame?task=T0`).  For more complex keywords (e.g. `details` for subtasks), python's [urllib.parse.urlencode](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) can be used to translate a keyword list into the proper url encoding.

The documentation will be built and available on the `/docs` route.

### Build/run the app in docker locally
To run a local version use:
```bash
docker compose build
docker compose up
```
and listen on `localhost:4000`.

### Running tests in the docker container
To run the tests use:
```bash
docker compose run --rm aggregation coverage run -m pytest && coverage report
```
