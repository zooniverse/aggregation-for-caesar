from collections import Iterable
from json import dumps as jsonify
from os import environ
from panoptes_client import Panoptes, User
import requests


class ConfigurationError(Exception):
    pass


known_params = [
    'destination'
]

connected = False

users = {}

destinations = {
    'mast': 'https://mast-forward.zooniverse.org/',
    'mockable': 'https://demo1580318.mockable.io/mast'
}


def userify(all_args, target_object):
    global users
    find_fields = _discover_fields(all_args)
    destination = all_args.get('destination')

    _stuff_object(target_object, find_fields)
    users = {}

    if destination:
        _forward_contents(target_object, destination)

    return jsonify(target_object)


def _forward_contents(payload, destination):
    if destination not in destinations:
        raise ConfigurationError('Unknown destination')

    requests.post(url=destinations[destination], json=payload)
    return


def _stuff_object(target_object, find_fields):
    for key in target_object.keys():
        if type(target_object[key]) is dict:
            _stuff_object(target_object[key], find_fields)

    user_ids = _discover_user_ids(target_object)
    for user_id in user_ids:
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
    global connected
    if user_id in users:
        user = users[user_id]
    else:
        if not connected:
            Panoptes.connect(endpoint='https://panoptes.zooniverse.org/', client_id=environ['FLASK_PANOPTES_ID'], client_secret=environ['FLASK_PANOPTES_SECRET'])
            connected = True
        user = User.find(user_id)
        users[user_id] = user

    return user
