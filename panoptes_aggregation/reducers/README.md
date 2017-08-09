# How to add a new reducer

## Make new functions for the reducer
Typically two function need to be defined for a reducer.

1. `process_data` is a helper function that takes a list of raw extracted data objects and pre-processes them into a form the main reducer function can use (e.g. arranging the data into arrays, creating `Counter` objects, etc...)
2. The `*_reducer` function that takes in the output of the `process_data` function and returns the reduced data as a `dict`-like object.
3. The `*_reducer` function should use the `@reducer_wrapper` decorator with the `process_data` function passed as the `process_data` keyword.
4. If the reducer exposes keywords the user can specify a `DEFAULTS` dictionary must be specified of the form:
```python
DEFAULTS = {
    'pairs': {'default': False, 'type': bool}
}
```
5. If these keywords are passed into the `process_data` function they should be added via the `@reducer_wrapper` with the `defaults_process` keyword.  If the keywords are passed to the `*_reducer` function they should be passed into the decorator with the `defaults_data` keyword.
6. Write tests for all the above functions and place them in the `test/reducer_test/` folder.  The decorator exposes the original function on the `._original` method of the decorated function, this allows for it to be tested directly.

### The `@reducer_wrapper` decorator

This decorator removes the boiler plate needed to set up a reducer function to work with extractions from either a `csv` file (offline) or an API request from caesar.  It will also run an optional `process_data` data function and pass the results into the wrapped function.  Various user defined keywords are also passed into either the `process_data` function or the wrapped function.  All keywords are parsed and type-checked before being used, that way no invalid keywords will be passed into either function.  Additionally the extracts from caesar are in a slightly different format than a list of raw extracts, the decorator will take this into account and re-format the caesar extract into a raw extract.  For reference the different syntax are:

Raw extract format:
```json
[
  {"a": 1, "b": 1},
  {"a": 1},
  {"b": 1, "c": 1},
  {"b": 1, "a": 1}
]
```

Caesar extract format:
```json
[
  {"data": {"a": 1, "b": 1}},
  {"data": {"a": 1}},
  {"data": {"b": 1, "c": 1}},
  {"data": {"b": 1, "a": 1}}
]
```

## Create the route to the reducer
The routes are automatically constructed using the `reducers` dictionary in the `__init__.py` file:

1. import the new reducer into the `__init__.py` file with the following format `from .q*_reducer import *_reducer`
2. Add the `*_reducer` function to the `reducer` dictionary with a sensible route name as the `key` (typically the `key` should be the same as the reducer name)

## Make sure everything still works
1. run `nosetests` and ensure all tests still pass
