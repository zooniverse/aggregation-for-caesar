'''Unility used for transforming a list of extracted data for use in tests'''
import copy


def extract_in_data(extracted_data):
    extracted_request_data = []
    for data in extracted_data:
        extracted_request_data.append({'data': copy.deepcopy(data)})
    return extracted_request_data
