import pandas
import json


def flatten_data(data, json_column='data'):
    json_data = data.pop(json_column)
    flat_data = pandas.io.json.json_normalize(json_data)
    # rename the columns so they can be un-flattened later
    flat_data.columns = ['{0}.{1}'.format(json_column, i) for i in flat_data.columns.values]
    other_data = pandas.DataFrame(data)
    return pandas.concat([other_data, flat_data], axis=1)


def unflatten_data(data, json_column='data'):
    data_dict = {}
    for name, value in data.iteritems():
        if ('{0}.'.format(json_column) in name) and (pandas.notnull(value)):
            key = name.split('{0}.'.format(json_column))[1]
            try:
                data_dict[key] = json.loads(value.replace('\'', '\"'))
            except:
                data_dict[key] = value
    return data_dict


def json_non_null(value):
    if pandas.notnull(value):
        try:
            return json.loads(value)
        except TypeError:
            return value
    else:
        return value


def unjson_dataframe(data_frame, json_column='data'):
    for column_name in data_frame.columns.values:
        if ('{0}.'.format(json_column) in column_name):
            data_frame[column_name] = data_frame[column_name].apply(json_non_null)
