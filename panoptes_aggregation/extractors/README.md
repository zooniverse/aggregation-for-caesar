# How to add a new extractor

## Make new functions for the extractor
At least two function must be defined for the extractor:

1. `classification_to_extract` takes in the raw classification json and returns the extracted data as a `dict`-like object
2. `*_extractor_request` takes in a Flask request and passes the payload to the above function
3. Write tests for both functions and place them in the `test/extractor_test/` folder

## Create the route to the extractor
The routes are automatically constructed using the `extractors` dictionary in the `__init__.py` file:

1. import the new extractor
2. Add the `*_extractor_request` function to the `extractors` dictionary with a sensible route name as the `key`
3. Add the `classification_to_extract` function to the `extractors_base` dictionary with the same `key` (this is used in the offline version of the code)

## Allow the offline version of the code automatically detect this extractor type from a workflow object

1. Update the `workflow_extractor_config.py` function with the new task type.  The value used for the type should be the same `key` used in the `__init__.py` file
2. Update the `tests/extractor_tests/test_workflow_extractor_config.py` class with this new task type

## Make sure everything still works
1. run `nosetests` and ensure all tests still pass
