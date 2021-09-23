'''
Panoptes Userify
------------------
This module provides a function to Fetch specific information from panoptes
about all users whose ids appear in the provided object.
'''
from collections.abc import Iterable
from json import dumps as jsonify
from os import getenv
from panoptes_client import Panoptes, User
from panoptes_client.panoptes import PanoptesAPIException
from yaml import safe_load
import requests


class ConfigurationError(Exception):
    '''Indicates that no destination was provided or an unknown destination was provided
    '''
    pass


# arg fields that contain non user lookup fields, i.e. the destination service 'mast'
reserved_params = ['destination']
# allow list of allowed fields args for API user resource lookups
allowed_user_fields = ['credited_name', 'display_name', 'id', 'login']
# restricted service_payload key value pairs
restricted_payload_keys = ['reducer_key']

users = {}

destinations = None


def userify(all_args, service_payload):
    '''Augment `service_payload` with panoptes user data specified in `all_args` and post it to the specified endpoint

    Parameters
    ----------
    all_args : dict
        A dictionary containing the key/value pairs from the querystring;
        these represent either certain predefined fields like destination
        or the names of fields to be retrieved from the `User` objects

    service_payload : dict
        A dictionary containing an object vivified from a JSON string in
        the request body. This entire object graph will be searched for
        all occurrences of `user_id` and `user_ids` and any object that has
        either will be populated with a `users` array containing the
        requested fields

    Returns
    -------
    service_payload : dict
        The original service_payload object, augmented with User arrays for each object
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

    allowed_user_lookup_fields = _discover_user_lookup_fields(all_args)
    destination = all_args.get('destination')

    # remove restricted payload data before sending to destination (mast)
    # https://github.com/zooniverse/caesar/pull/1342#issuecomment-917096083
    for restriced_key in restricted_payload_keys:
        service_payload.pop(restriced_key, None)

    _stuff_object(service_payload, allowed_user_lookup_fields)
    users = {}

    if destination:
        _forward_contents(service_payload, destination)

    return jsonify(service_payload)


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

    return requests.post(**request_args, timeout=5)


def _stuff_object(service_payload, find_fields):
    for key in service_payload.keys():
        if type(service_payload[key]) is dict:
            _stuff_object(service_payload[key], find_fields)

    user_ids = _discover_user_ids(service_payload)
    for user_id in user_ids:
        if not user_id:
            continue

        user = _retrieve_user(user_id)
        service_payload['users'] = service_payload.get('users', [])
        service_payload['users'].append(_build_user_hash(user, find_fields))

    return service_payload


def _discover_user_lookup_fields(request_args):
    request_args = request_args.keys()
    # filter any reserved params and only allow specific user fields for the API lookup
    # e.g. avoid leaking the email field if we can read it from the API
    return [i for i in request_args if i not in reserved_params and i in allowed_user_fields]


def _discover_user_ids(service_payload):
    user_ids = []
    if 'user_ids' in service_payload:
        user_ids = service_payload['user_ids']
    if 'user_id' in service_payload:
        user_ids.append(service_payload['user_id'])

    flattened_user_ids = _unique(_flatten(user_ids))
    if flattened_user_ids:
        # if we found some user_ids then we should connect the API client
        # for the user lookups
        connect_api_client()

    return flattened_user_ids


def _build_user_hash(user, find_fields):
    user_hash = {'id': user.id}
    for key in find_fields:
        # add a default return for user that are not found
        # in panoptes
        user_hash[key] = getattr(user, key, "None")
    return user_hash


def _unique(l):
    return list(set(l))


def _flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from _flatten(el)
        else:
            yield el


class CantFindUser():
    def __init__(self, id):
        self.id = id


def connect_api_client():
    # connect to the API only once for this function request
    Panoptes.connect(
        endpoint=getenv('PANOPTES_URL', 'https://panoptes.zooniverse.org/'),
        client_id=getenv('PANOPTES_CLIENT_ID'),
        client_secret=getenv('PANOPTES_CLIENT_SECRET')
    )


def _retrieve_user(user_id):
    if user_id in users:
        user = users[user_id]
    else:
        try:
            user = User.find(user_id)
        except PanoptesAPIException:
            # some users are not found in panoptes
            # return an empty class with an `id` attribute
            user = CantFindUser(user_id)
        users[user_id] = user

    return user
