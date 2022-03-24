'''
Nfn Extractor
---------------
This module provides functions to answer certain questions about a Notes from Nature
annotation for use in their Field Book.
'''
from .extractor_wrapper import extractor_wrapper

import collections.abc
from dateutil.parser import parse as dateparse
from datetime import timedelta


class ClassificationParser(object):
    '''A classification parser'''

    def __init__(self, classification, kwargs):
        self.classification = classification
        self.created_at = self.classification['created_at']
        self.params = kwargs
        self.subject_metadata = {
            k.lower(): v for k, v in classification['subject']['metadata'].items()
        }
        self.metadata = {
            k.lower(): v for k, v in classification['metadata'].items()
        }
        self.tasks = self.flatten(classification['annotations'])

    def iterable(self, arg):
        return (
            isinstance(arg, collections.abc.Iterable)
            and not isinstance(arg, str)
        )

    def flatten(self, anno):
        f = {}
        for a in anno:
            f[a['task']] = a['value']
            if (self.iterable(a['value'])):
                for subanno in a['value']:
                    if isinstance(subanno, dict) and 'task' in subanno:
                        f[subanno['task']] = subanno['value']
        return f

    def get_basic(self, label):
        if label in self.subject_metadata:
            return self.subject_metadata[label]
        else:
            task = self.params[label]
            if task in self.tasks:
                value = self.tasks[task]
                try:
                    return value[0]['value']
                except TypeError:
                    return value
            else:
                return None


def check_decade(parser):
    year = parser.get_basic('year')
    if year and len(str(year)) == 4:
        return "%s0s" % str(year)[-2]
    else:
        return None


def check_time(parser):
    pre_time = dateparse(parser.created_at)
    time = pre_time + timedelta(seconds=int(parser.metadata["utc_offset"]))
    # from nose.tools import set_trace; set_trace()
    if 3 <= time.hour < 9:
        return "earlybird"
    elif 9 <= time.hour < 15:
        return "lunchbreak"
    elif 15 <= time.hour < 21:
        return "dinnertime"
    else:
        return "nightowl"


def earth_day(parser):
    date = dateparse(parser.created_at)
    if date.day == 22 and date.month == 4:
        return True
    else:
        return None


def we_dig_bio(parser):
    date = dateparse(parser.created_at)
    if (date.year == 2020) and (date.month == 10) and (15 <= date.day <= 18):
        return 2020
    elif (date.year == 2021) and (date.month == 4) and (8 <= date.day <= 11):
        return 2021
    elif (date.year == 2021) and (date.month == 10) and (14 <= date.day <= 17):
        return 2021
    elif (date.year == 2022) and (date.month == 4) and (7 <= date.day <= 10):
        return 2022
    elif (date.year == 2022) and (date.month == 10) and (13 <= date.day <= 16):
        return 2022
    else:
        return None


@extractor_wrapper()
def nfn_extractor(classification, **kwargs):
    response = {}
    if len(classification['annotations']) > 0:
        parser = ClassificationParser(classification, kwargs)

        if 'workflow' in parser.params:
            response['workflow'] = parser.params['workflow']
        if 'year' in parser.params:
            response['decade'] = check_decade(parser)
        if 'country' in parser.params:
            response['country'] = parser.get_basic('country')
        if 'state' in parser.params:
            response['state'] = parser.get_basic('state')

        response['time'] = check_time(parser)
        response['earth_day'] = earth_day(parser)
        response['we_dig_bio'] = we_dig_bio(parser)

    return {k: v for k, v in response.items() if v is not None}
