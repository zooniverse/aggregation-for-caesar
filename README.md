# Getting started

This is a collection of external reducers written for [caesar](https://github.com/zooniverse/caesar) and offline use.

---

## Documentation
You can find the [latest documentation](https://aggregation-caesar.zooniverse.org/docs) on the aggregations code's website.

---

## Installing for offline use
### With your own python install (python 3 only)
Instal the latest stable release:
```bash
pip install panoptes_aggregation
```

Or for development or testing, you can install the development version directly from GitHub:
```bash
pip install -U git+git://github.com/zooniverse/aggregation-for-caesar.git
```

Upgrade and existing installation:
```bash
pip install -U panoptes_aggregation
```

If you see an error about `Cython` not being installed run `pip install cython` and try `pip install .` again.

### With Docker
[https://docs.docker.com/get-started/](https://docs.docker.com/get-started/)

**Using docker-compose** [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
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

---

## Installing for online use
The docker file included is ready to be deployed on any server.  Once deployed, the extractors will be available on the `/extractors/<name of extractor function>` routes and the reducers will be available on the `/reducers/<name of reducer function>` routes.  Any keywords passed into these functions should be included as url parameters on the route (e.g. `https://aggregation-caesar.zooniverse.org/extractors/point_extractor_by_frame?task=T0`).  For more complex keywords (e.g. `detals` for subtasks), python's [urllib.parse.urlencode](https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlencode) can be used to translate a keyword list into the proper url encoding.

The documentation will be built and available on the `/docs` route.

### Build/run the app in docker locally
To run a local version use:
```bash
docker-compose build
docker-compose up
```
and listen on `localhost:5000`.

### Running tests in the docker container
To run the tests use:
```bash
docker-compose run --rm aggregation nosetests
```
