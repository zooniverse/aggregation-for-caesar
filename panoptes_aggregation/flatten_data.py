import pandas
import json


def flatten_data(data, json_column='data'):
    json_data = data.pop(json_column)
    flat_data = pandas.io.json.json_normalize(json_data)
    # rename the columns so they can be un-flattened later
    flat_data.columns = ['data.{0}'.format(i) for i in flat_data.columns.values]
    other_data = pandas.DataFrame(data)
    return pandas.concat([other_data, flat_data], axis=1)


def unflatten_data(data):
    data_dict = {}
    for name, value in data.iteritems():
        if ('data.' in name) and (value is not pandas.np.nan):
            key = name.split('data.')[1]
            data_dict[key] = json.loads(value)
    return data_dict
