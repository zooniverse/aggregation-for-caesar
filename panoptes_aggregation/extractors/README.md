# How to add a new extractor

## Make a new function for the extractor

1. Create a new file for the function in the `extractors` folder
2. Define a new function `*_extractor` that takes in the raw classification json (as it appears in the classification dump `csv` from Panoptes) and returns a `dict`-like object of the extracted data.
3. Use the `@extractor_wrapper` decorator on the function (can be imported with `from .extractor_wrapper import extractor_wrapper`).
4. Write tests for the extractor and place it in the `tests/extractor_tests` folder, there should be at least two tests, on for a raw classification being passed into the function and the other for a API `request` being passed in (see existing tests for formatting the request framework correctly).

### The `@extractor_wrapper` decorator

This decorator removes the boiler plate code that goes along with making a extractor function that works with both the classification dump `csv` files (offline) and API request from caesar (online).  If A `request` is passed into the function it will pull the data out as json and pass it into the extractor, if anything else is passed in the function will be called directly.  Additionally caesar passes the classification in with a slightly different syntax, this wrapper will unpack it back into the raw classification format before passing it into the extractor.  For reference the two syntax are:

Raw classification format
```json
{
  "annotations": [{
      "task": "T0",
      "task_label": "A single question",
      "value": "Yes"
  }]
}
```

Caesar classification format
```json
{
  "annotations": [{
      "T0": [{
        "task": "T0",
        "task_label": "A single question",
        "value": "Yes"
      }]
  }]
}
```

## Create the route to the extractor
The routes are automatically constructed using the `extractors` dictionary in the `__init__.py` file:

1. import the new extractor into the `__init__.py` file with the following format `from .*_extractor import *_extractor`
2. Add the `*_extractor` function to the `extractors` dictionary with a sensible route name as the `key` (typically the `key` should be the same as the extractor name)

## Allow the offline version of the code automatically detect this extractor type from a workflow object

1. Update the `workflow_extractor_config.py` function with the new task type.  The value used for the type should be the same `key` used in the `__init__.py` file
2. Update the `tests/extractor_tests/test_workflow_extractor_config.py` class with this new task type

## Add to documentation
The code is auto-documented using [sphinx](http://www.sphinx-doc.org/en/stable/index.html).

1. Add a doc string to every function written and a "heading" doc string at the top of any new files created (follow the [numpy doc string convention](https://github.com/numpy/numpy/blob/master/doc/HOWTO_DOCUMENT.rst.txt))
2. Add a reference to the new file to `doc/source/extractors.rst`
3. Build the docs with `./make_docs.sh`

## Make sure everything still works
1. run `nosetests` and ensure all tests still pass
