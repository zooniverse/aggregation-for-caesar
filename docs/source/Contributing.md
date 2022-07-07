# Contributing

## Code Style
[PEP8](https://www.python.org/dev/peps/pep-0008/) style is used in most cases and flake8 is used for linting by running `flake8` in the source directory.  The `setup.cfg` contains the configuration for the linter and lists the error codes and files that are being ignored.

---

## Building Documentation
Automatic documentation will be created using [sphinx](http://www.sphinx-doc.org/en/stable/) so add doc strings to any files created and functions written.  Documentation can be compiled with the `make_docs.sh` bash script.

---

## Writing Extractors
Extractors are used to take classifications coming out of Panoptes and extract the relevant data needed to calculate a aggregated answer for one task on a subject.  Ideally this extraction should be as flat as possible (i.e. no deeply nested dictionaries), but sometimes this can not be avoided.

### 1. Make a new function for the extractor

1. Create a new file for the function in the `extractors` folder
2. Define a new function `*_extractor` that takes in the raw classification json (as it appears in the classification dump `csv` from Panoptes) and returns a `dict`-like object of the extracted data.
3. Use the `@extractor_wrapper` decorator on the function (can be imported with `from .extractor_wrapper import extractor_wrapper`).
4. Use the `@subtask_wrapper` and `@tool_wrapper` decorators if the function is for a drawing tool (can be imported with `from .extractor_wrapper import subtask_extractor_wrapper`).
5. Write tests for the extractor in the `tests/extractor_tests` folder.  The `ExtractorTest` class from the `tests/extractor_tests/base_test_class.py` file should be used to create the test function.  This class ensures that both the "offline" and "online" versions of the code are tested and produce the expected results.  See the other tests in that folder for examples of how to use the `ExtractorTest` class.

#### The `@extractor_wrapper` decorator

This decorator removes the boiler plate code that goes along with making a extractor function that works with both the classification dump `csv` files (offline) and API request from caesar (online).  If A `request` is passed into the function it will pull the data out as json and pass it into the extractor, if anything else is passed in the function will be called directly.  This decorator also does the following:
 - filter the classifications using the `task` and `tools` keywords passed into the extractor
 - add the aggregation version number to the final extract

#### The `@subtask_extractor_wrapper` decorator
This decorator removes the boiler plate code that goes along with extracting subtask data from drawing tasks.  This decorator looks for the `details` keyword passed into the extractor function and will apply the specified extractor the the proper subtask data and return the extracts as a list in the same order the subtask presented them.

Note: It is assumed that the first level of the extracted dictionary refers to the subject's frame index (e.g. `frame0` or `frame1`) even when the subject only has one frame.

#### The `@tool_wrapper` decorator
This decorator removes the boiler plate code for filtering classifications based on the `tools` keyword.  This makes it so each tool for a drawing task can have extractors set up independently.

### 2. Create the route to the extractor
The routes are automatically constructed using the `extractors` dictionary in the `__init__.py` file:

1. import the new extractor into the `__init__.py` file with the following format `from .*_extractor import *_extractor`
2. Add the `*_extractor` function to the `extractors` dictionary with a sensible route name as the `key` (typically the `key` should be the same as the extractor name)

### 3. Allow the offline version of the code automatically detect this extractor type from a workflow object

1. Update the `workflow_config.py` function with the new task type.  The value used for the type should be the same `key` used in the `__init__.py` file
2. Update the `tests/utility_tests/test_workflow_config.py` test with this new task type

### 4. Add to documentation
The code is auto-documented using [sphinx](http://www.sphinx-doc.org/en/stable/index.html).

1. Add a doc string to every function written and a "heading" doc string at the top of any new files created (follow the [numpy doc string convention](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard))
2. Add a reference to the new file to `docs/source/extractors.rst`
3. Add to the extractor/reducer lookup table `docs/source/Task_lookup_table.rst`
4. Build the docs with the `make_docs.sh` bash script

### 5. Make sure everything still works
1. run `nosetests` and ensure all tests still pass
2. (optional) `nosetests --cover-html` to compile an html page for checking what parts of the code are not covered

---

## Writing Reducers
Reducers are functions that take a list of extracts and combines them into aggregated values.  Ideally this reduction should be as flat as possible (i.e. no deeply nested dictionaries), but sometimes this can not be avoided.

### 1. Make new functions for the reducer
Typically two function need to be defined for a reducer.

1. `process_data` is a helper function that takes a list of raw extracted data objects and pre-processes them into a form the main reducer function can use (e.g. arranging the data into arrays, creating `Counter` objects, etc...)
2. The `*_reducer` function that takes in the output of the `process_data` function and returns the reduced data as a `dict`-like object.
3. The `*_reducer` function should use the `@reducer_wrapper` decorator with the `process_data` function passed as the `process_data` keyword.
4. If the reducer exposes keywords the user can specify a `DEFAULTS` dictionary must be specified of the form: `DEFAULTS = {'<keyword name>': {'default': <default value>, 'type': <data type>}}`
5. If these keywords are passed into the `process_data` function they `DEFAULTS` dictionary should be passed into the `@reducer_wrapper` as the `defaults_process` keyword.  If these keywords are passed into the main `*_reducer` function the `DEFAULTS` dictionary should be passed into the `@reducer_wrapper` as the `defaults_data` keyword.  Note: any combination of these two can be used.
6. Write tests for all the above functions and place them in the `test/reducer_test/` folder.  The decorator exposes the original function on the `._original` method of the decorated function, this allows for it to be tested directly.  The `ReducerTest` class from the `tests/reducer_tests/base_test_class.py` file should be used to create the test function.  This class ensures that both the "offline" and "online" versions of the code are tested and produce the expected results.  See the other tests in that folder for examples of how to use the `ReducerTest` class.

#### The `@reducer_wrapper` decorator

This decorator removes the boiler plate needed to set up a reducer function to work with extractions from either a `csv` file (offline) or an API request from caesar.  It will also run an optional `process_data` data function and pass the results into the wrapped function.  Various user defined keywords are also passed into either the `process_data` function or the wrapped function.  All keywords are parsed and type-checked before being used, that way no invalid keywords will be passed into either function.  This wrapper will also do the following:
 - Remove the `aggregation_version` keyword from each extract so it is not passed into the reducer function
 - Add the `aggregation_version` keyword to the final reduction dictionary

#### The `@subtask_reducer_wrapper` decorator
This decorator removes the boiler plate code that goes along with reducing subtask data from drawing tasks.  This decorator looks for the `details` keyword passed into the reducer function and will apply the specified reducer the the proper subtask data within each *cluster* found on the subject and returns the reductions as a list in the same order the subtask presented them.

Note: It is assumed that the first level of the reduced dictionary refers to the subject's frame index (e.g. `frame0` or `frame1`) even when the subject only has one frame.

### 2. Create the route to the reducer
The routes are automatically constructed using the `reducers` dictionary in the `__init__.py` file:

1. import the new reducer into the `__init__.py` file with the following format `from .*_reducer import *_reducer`
2. Add the `*_reducer` function to the `reducer` dictionary with a sensible route name as the `key` (typically the `key` should be the same as the reducer name)

### 3. Add to documentation
The code is auto-documented using [sphinx](http://www.sphinx-doc.org/en/stable/index.html).

1. Add a doc string to every function written and a "heading" doc string at the top of any new files created (follow the [numpy doc string convention](https://numpydoc.readthedocs.io/en/latest/format.html#docstring-standard))
2. Add a reference to the new file to `docs/source/reducers.rst`
3. Add to the extractor/reducer lookup table `docs/source/Task_lookup_table.rst`
4. Build the docs with the `make_docs.sh` bash script

### 4. Make sure everything still works
1. run `nosetests` and ensure all tests still pass (coverage is automatically reported)
2. (optional) `nosetests --cover-html` to compile an html page for checking what parts of the code are not covered

---

## Copying extractors and reducers

Sometimes it is useful to have two extractor/reducers routes point to the same underlying function (e.g. question and shortcut tasks), to ensure separate `csv` files are created in offline mode.  Unfortunately if you just place the same function multiple times in the `extractors/__init__.py` or `reducers/__init__.py` dictionaries `flask` will crash since two routes point to functions with the same name.  To help with this `panoptes_aggregation.copy_function.copy_function` can be used to clone any function with a new name:

```python
from panoptes_aggregation.copy_function import copy_function

new_function = copy_function(old_function, 'new_name')
```
