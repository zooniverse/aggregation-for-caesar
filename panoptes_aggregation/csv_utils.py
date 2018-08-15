import ast
import pandas
from pandas.io.json.normalize import nested_to_record


def flatten_data(data, json_column='data'):
    json_data = data.pop(json_column)
    # this gets at any nested dicts as well
    flat_data = pandas.DataFrame(nested_to_record(json_data))
    # rename the columns so they can be un-flattened later
    flat_data.columns = ['{0}.{1}'.format(json_column, i) for i in flat_data.columns.values]
    other_data = pandas.DataFrame(data)
    return pandas.concat([other_data, flat_data], axis=1)


def unflatten_data(data, json_column='data', renest=True):
    data_dict = {}
    for name, value in data.iteritems():
        if ('{0}.'.format(json_column) in name) and (pandas.notnull(value)):
            key = name.split('{0}.'.format(json_column))[1]
            try:
                data_dict[key] = ast.literal_eval(value)
            except:
                data_dict[key] = value
    if renest:
        return renest_dict(data_dict)
    else:
        return data_dict


def nested_set(dic, keys, value):
    for key in keys[:-1]:
        dic = dic.setdefault(key, {})
    dic[keys[-1]] = value


def renest_dict(data, seporator='.'):
    output = {}
    for key, value in data.items():
        key_expand = key.split(seporator)
        nested_set(output, key_expand, value)
    return output


def json_non_null(value):
    if pandas.notnull(value):
        try:
            return ast.literal_eval(value)
        except:
            return value
    else:
        return value


def unjson_dataframe(data_frame, json_column='data'):
    for column_name in data_frame.columns.values:
        if ('{0}.'.format(json_column) in column_name):
            data_frame[column_name] = data_frame[column_name].apply(json_non_null)


def move_to_front(list_in, value):
    list_copy = list_in[:]
    if value in list_in:
        list_copy.remove(value)
        list_copy = [value] + list_copy
    return list_copy


def order_columns(data_frame, json_column='data', front=['choice']):
    cols = data_frame.columns.tolist()
    d_cols = [c for c in cols if '{0}.'.format(json_column) in c]
    d_cols.sort()
    for f in front[::-1]:
        d_cols = move_to_front(d_cols, '{0}.{1}'.format(json_column, f))
    order_columns = cols[:-len(d_cols)] + d_cols
    return data_frame[order_columns]
