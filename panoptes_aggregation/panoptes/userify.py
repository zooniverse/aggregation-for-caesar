'''
Panoptes Userify
------------------
This module provides a function to Fetch specific information from panoptes
about all users whose ids appear in the provided object.
'''
from collections import Iterable
from json import dumps as jsonify
from os import getenv
from panoptes_client import Panoptes, User
from yaml import safe_load
import requests


class ConfigurationError(Exception):
    '''Indicates that no destination was provided or an unknown destination was provided
    '''
    pass


known_params = ['destination']

users = {}

destinations = None


def userify(all_args, target_object):
    '''Augment `target_object` with panoptes user data specified in `all_args` and post it to the specified endpoint

    Parameters
    ----------
    all_args : dict
        A dictionary containing the key/value pairs from the querystring;
        these represent either certain predefined fields like destination
        or the names of fields to be retrieved from the `User` objects

    target_object : dict
        A dictionary containing an object vivified from a JSON string in
        the request body. This entire object graph will be searched for
        all occurrences of `user_id` and `user_ids` and any object that has
        either will be populated with a `users` array containing the
        requested fields

    Returns
    -------
    target_object : dict
        The original object, augmented with User arrays for each object
        in the object graph with a `user_id` or `user_ids` field.

    Examples
    --------
    >>> userify({'login': None, 'destination': 'mast'}, {
        'some_field': 'some_value',
        'user_ids': [[1, 2], 3],
        'another_field': 'another_value'
    })
    {
        'some_field': 'some_value',
        'user_ids': [[1, 2], 3],
        'another_field': 'another_value',
        'users': [
            {'id': 1, 'login': 'login 1'},
            {'id': 2, 'login': 'login 2'},
            {'id': 3, 'login': 'login 3'}
        ]
    }
    '''
    global users
    find_fields = _discover_fields(all_args)
    destination = all_args.get('destination')

    _stuff_object(target_object, find_fields)
    users = {}

    if destination:
        _forward_contents(target_object, destination)

    return jsonify(target_object)


def _read_config():  # pragma: no cover
    with open('endpoints.yml', mode='r') as f:
        return safe_load(f)


def _forward_contents(payload, destination):
    global destinations

    if not destinations:
        destinations = _read_config()['endpoints']

    if destination not in destinations:
        raise ConfigurationError('Unknown destination')

    endpoint = destinations[destination]
    request_args = {
        'url': endpoint['url'],
        'json': payload,
    }

    if 'auth-header' in endpoint:
        request_args['headers'] = {
            endpoint['auth-header']: getenv(endpoint['auth-token'])
        }

    return requests.post(**request_args)


def _stuff_object(target_object, find_fields):
    for key in target_object.keys():
        if type(target_object[key]) is dict:
            _stuff_object(target_object[key], find_fields)

    user_ids = _discover_user_ids(target_object)
    for user_id in user_ids:
        if not user_id:
            continue

        user = _retrieve_user(user_id)
        target_object['users'] = target_object.get('users', [])
        target_object['users'].append(_build_user_hash(user, find_fields))

    return target_object


def _discover_fields(request_args):
    raw_list = request_args.keys()
    return [i for i in raw_list if i not in known_params]


def _discover_user_ids(target_object):
    user_ids = []
    if 'user_ids' in target_object:
        user_ids = target_object['user_ids']
    if 'user_id' in target_object:
        user_ids.append(target_object['user_id'])

    return _unique(_flatten(user_ids))


def _build_user_hash(user, find_fields):
    user_hash = {'id': user.id}
    for key in find_fields:
        user_hash[key] = getattr(user, key)
    return user_hash


def _unique(l):
    return list(set(l))


def _flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from _flatten(el)
        else:
            yield el


def _retrieve_user(user_id):
    if user_id in users:
        user = users[user_id]
    else:
        Panoptes.connect(
            endpoint=getenv('PANOPTES_URL', 'https://panoptes.zooniverse.org/'),
            client_id=getenv('PANOPTES_CLIENT_ID'),
            client_secret=getenv('PANOPTES_CLIENT_SECRET')
        )

        user = User.find(user_id)
        users[user_id] = user

    return user
