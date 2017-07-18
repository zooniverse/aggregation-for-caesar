# How to add a new reducer

## Make new functions for the reducer
At least four functions must be defined for the reducer:

1. `process_data` is a helper function that takes a list of extracted data objects and pre-processes them into a form the main reducer function can use (e.g. arranging the data into arrays, creating `Counter` objects, etc...)
2. The main reducer function that takes the output of `process_data` and returns the reduced data object
3. If the reducer exposes keywords the user can specify a `DEFAULTS` dictionary must be specified of the form:
```python
DEFAULTS = {
    'pairs': {'default': False, 'type': bool}
}
```
3. `*_reducer_request` takes in a Flask request, process keywords with the `process_kwargs` function with `DEFAULTS` passed as the second argument, process the data with `process_data`, and runs the main reducer.
4. `reducer_base` does the same as the above function but takes in a list of the extracted data and the user keywords instead of a Flask request
5. Write tests for all the above functions and place them in the `test/reducer_test/` folder

## Create the route to the reducer
The routes are automatically constructed using the `reducers` dictionary in the `__init__.py` file:

1. import the new reducer
2. Add the `*_reducer_request` function to the `reducer` dictionary with a sensible route name as the `key`
3. Add the `reducer_base` function to the `reducer_base` dictionary with the same `key` (this is used in the offline version of the code)

## Make sure everything still works
1. run `nosetests` and ensure all tests still pass
