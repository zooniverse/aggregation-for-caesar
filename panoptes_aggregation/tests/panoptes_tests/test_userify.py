from importlib import import_module
from unittest.mock import MagicMock, PropertyMock, Mock, patch
from nose.tools import assert_equal, assert_raises, assert_count_equal, assert_is_instance
import requests
import unittest

import os
from os import environ

try:
    from panoptes_client import Panoptes, User
    from panoptes_client.panoptes import PanoptesAPIException
    panoptes = import_module('panoptes_aggregation.panoptes', __name__).panoptes_testing
    # make the API client connect call a no-op for all tests
    Panoptes.connect = Mock()
    OFFLINE = False
except ImportError:
    OFFLINE = True


environ.setdefault('AGGREGATION_PANOPTES_ID', 'TEST')
environ.setdefault('AGGREGATION_PANOPTES_SECRET', 'TEST')


def build_mock_user(**kwargs):
    mock_user = MagicMock()
    for key, value in kwargs.items():
        setattr(type(mock_user), key, PropertyMock(return_value=value, create=True))
    return mock_user


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_userify():
    panoptes._read_config = Mock(return_value={
        'endpoints': {
            'mockable': {
                'url': 'https://demo1580318.mockable.io/mast',
            },
            'mast': {
                'url': 'https://mast-forwarder.zooniverse.org/',
                'auth-header': 'X-ASB-AUTH',
                'auth-token': 'MAST_AUTH_TOKEN',
            },
        }
    })

    # doesn't choke if nothing to do
    assert_equal(panoptes.userify({}, {'foo': 'bar'}), '{"foo": "bar"}')
    assert_equal(panoptes.userify({'login': None}, {'foo': 'bar'}), '{"foo": "bar"}')
    assert_equal(panoptes.userify({}, {}), '{}')
    assert_equal(panoptes.userify({'login': None}, {}), '{}')

    # removes restricted payload key/value pairs
    assert_equal(panoptes.userify({'login': None}, {'reducer_key': 'T0', 'id': '1'}), '{"id": "1"}')

    # fills out object correctly
    (User.find) = Mock(return_value=build_mock_user(id=3, login="login 3"))
    assert_equal(panoptes.userify({'login': None}, {'user_id': 3}), '{"user_id": 3, "users": [{"id": 3, "login": "login 3"}]}')

    # forwards appropriately
    requests.post = MagicMock()
    assert_equal(panoptes.userify({'login': None, 'destination': 'mockable'}, {'user_id': 3}), '{"user_id": 3, "users": [{"id": 3, "login": "login 3"}]}')
    (requests.post).assert_called_once()


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_unique():
    # removes duplicate elements
    assert_count_equal(panoptes._unique([]), [])
    assert_count_equal(panoptes._unique([3]), [3])
    assert_count_equal(panoptes._unique([3, 3]), [3])
    assert_count_equal(panoptes._unique([3, 3, 3]), [3])
    assert_count_equal(panoptes._unique([3, 4]), [3, 4])
    assert_count_equal(panoptes._unique([1, 1, 2, 3]), [1, 2, 3])
    assert_count_equal(panoptes._unique([1, 2, 3, 1]), [1, 2, 3])


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_flatten():
    # makes any combination of lists and not-lists into a single flat list
    assert_count_equal(list(panoptes._flatten([])), [])
    assert_count_equal(list(panoptes._flatten([1])), [1])
    assert_count_equal(list(panoptes._flatten([1, 2])), [1, 2])
    assert_count_equal(list(panoptes._flatten([1, [2]])), [1, 2])
    assert_count_equal(list(panoptes._flatten([[1], 2])), [1, 2])
    assert_count_equal(list(panoptes._flatten([[1], [2]])), [1, 2])
    assert_count_equal(list(panoptes._flatten([1, [2], 3])), [1, 2, 3])
    assert_count_equal(list(panoptes._flatten([1, [2], 2])), [1, 2, 2])
    assert_count_equal(list(panoptes._flatten([[1], 2, []])), [1, 2])
    assert_count_equal(list(panoptes._flatten([[1], [], 2])), [1, 2])


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_discover_user_lookup_fields():
    # can find list of allowd user fields
    allowed_user_fields = {'login': '', 'credited_name': '', 'display_name': '', 'id': ''}
    assert_count_equal(panoptes._discover_user_lookup_fields(allowed_user_fields), ['login', 'credited_name', 'display_name', 'id'])

    # ignores missing or not allowed known user fields
    assert_count_equal(panoptes._discover_user_lookup_fields({}), [])
    assert_count_equal(panoptes._discover_user_lookup_fields({'email': ''}), [])
    assert_count_equal(panoptes._discover_user_lookup_fields({'f1': 'v1', 'created_at': 'v2'}), [])
    assert_count_equal(panoptes._discover_user_lookup_fields({'f1': 'v1', 'destination': 'd1', 'f2': 'v2'}), [])

    # ignores known fields
    assert_count_equal(panoptes._discover_user_lookup_fields({'destination': 'v1'}), [])
    assert_count_equal(panoptes._discover_user_lookup_fields({'destination': 'v1', 'f2': 'v2'}), [])


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_build_user_hash():
    mock_user = build_mock_user(id=1, login='login', display_name='display_name')

    # fetches the specified properties and puts them in a hash
    assert_equal(panoptes._build_user_hash(mock_user, []), {'id': 1})
    assert_equal(panoptes._build_user_hash(mock_user, ['login']), {'id': 1, 'login': 'login'})
    assert_equal(panoptes._build_user_hash(mock_user, ['display_name']), {'id': 1, 'display_name': 'display_name'})
    assert_equal(panoptes._build_user_hash(mock_user, ['login', 'display_name']), {'id': 1, 'login': 'login', 'display_name': 'display_name'})


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_retrieve_user():
    mock_user1 = build_mock_user(id=1, login='login', display_name='display_name')
    mock_user2 = build_mock_user(id=2, login='login', display_name='display_name')

    # finds user by calling API
    User.find = Mock(return_value=mock_user1)
    found_user = panoptes._retrieve_user(1)
    assert_equal(found_user, mock_user1)
    assert_equal(found_user.id, 1)
    (User.find).assert_called_once_with(1)

    # uses cached user object when possible instead of finding it again
    User.find = Mock(return_value=mock_user2)
    found_user = panoptes._retrieve_user(1)
    assert_equal(found_user, mock_user1)
    assert_equal(found_user.id, 1)
    (User.find).assert_not_called()


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_retrieve_user_error():
    User.find = MagicMock(side_effect=[PanoptesAPIException('test')])
    found_user = panoptes._retrieve_user(10)
    assert_is_instance(found_user, panoptes.CantFindUser)
    assert_equal(found_user.id, 10)


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_discover_user_ids():
    # finds user_id if present
    assert_count_equal(panoptes._discover_user_ids({'foo': 'bar'}), [])
    assert_count_equal(panoptes._discover_user_ids({'user_id': 3}), [3])
    assert_count_equal(panoptes._discover_user_ids({'foo': 'bar', 'user_id': 3}), [3])

    # doesn't recurse into child objects
    assert_count_equal(panoptes._discover_user_ids({'foo': {'user_id': 3}}), [])

    # finds user_ids
    assert_count_equal(panoptes._discover_user_ids({'user_ids': [3, 4]}), [3, 4])

    # combines user_ids and user_id if both present
    assert_count_equal(panoptes._discover_user_ids({'user_ids': [3, 4], 'user_id': 5}), [3, 4, 5])


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def user_find_side_effect(*args, **_):
    user_id = args[0]
    return build_mock_user(id=user_id, login='login {0}'.format(user_id), display_name='display_name {0}'.format(user_id))


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_stuff_object():
    User.find = MagicMock(side_effect=user_find_side_effect)

    # doesn't crash on an empty object
    assert_equal(panoptes._stuff_object({}, []), {})
    assert_equal(panoptes._stuff_object({}, ['login']), {})

    # maintains existing properties
    assert_equal(panoptes._stuff_object({'foo': 'bar'}, ['login']), {'foo': 'bar'})
    assert_equal(panoptes._stuff_object({'foo': 'bar'}, []), {'foo': 'bar'})

    # builds a user even if no fields are requested
    assert_equal(panoptes._stuff_object({'user_id': 3}, []), {'user_id': 3, 'users': [{'id': 3}]})

    # adds requested fields
    assert_equal(panoptes._stuff_object({'user_id': 3}, ['login']), {'user_id': 3, 'users': [{'id': 3, 'login': 'login 3'}]})
    assert_equal(panoptes._stuff_object({'user_id': 3}, ['display_name']), {'user_id': 3, 'users': [{'id': 3, 'display_name': 'display_name 3'}]})
    assert_equal(panoptes._stuff_object({'user_id': 3}, ['login', 'display_name']), {'user_id': 3, 'users': [{'id': 3, 'display_name': 'display_name 3', 'login': 'login 3'}]})

    # finds fields in nested objects
    assert_equal(panoptes._stuff_object({'foo': {'user_id': 3}}, ['login', 'display_name']), {'foo': {'user_id': 3, 'users': [{'id': 3, 'display_name': 'display_name 3', 'login': 'login 3'}]}})

    # fetches multiple users if user_ids
    assert_equal(panoptes._stuff_object({'user_ids': [3, 4]}, []), {'user_ids': [3, 4], 'users': [{'id': 3}, {'id': 4}]})

    # handles null user ids
    assert_equal(panoptes._stuff_object({'user_ids': [3, None]}, []), {'user_ids': [3, None], 'users': [{'id': 3}]})

    # finds fields at multiple levels
    assert_equal(panoptes._stuff_object({'foo': {'user_id': 3}, 'user_id': 4}, []), {'foo': {'user_id': 3, 'users': [{'id': 3}]}, 'user_id': 4, 'users': [{'id': 4}]})


@unittest.skipIf(OFFLINE, 'Installed in offline mode')
def test_forward_contents():
    panoptes._read_config = Mock(return_value={
        'endpoints': {
            'mockable': {
                'url': 'https://demo1580318.mockable.io/mast',
            },
            'mast': {
                'url': 'https://mast-forwarder.zooniverse.org/',
                'auth-header': 'X-ASB-AUTH',
                'auth-token': 'MAST_AUTH_TOKEN',
            },
        }
    })

    # only will send to known endpoints
    requests.post = MagicMock()
    assert_raises(panoptes.ConfigurationError, lambda: panoptes._forward_contents('contents', None))
    assert_raises(panoptes.ConfigurationError, lambda: panoptes._forward_contents('contents', ''))
    assert_raises(panoptes.ConfigurationError, lambda: panoptes._forward_contents('contents', 'blah'))
    (requests.post).assert_not_called()

    # sends to known endpoints correctly
    requests.post = MagicMock()
    panoptes._forward_contents({'foo': 'bar'}, 'mockable')
    (requests.post).assert_called_once_with(timeout=5, url='https://demo1580318.mockable.io/mast', json={'foo': 'bar'})

    requests.post = MagicMock()
    with patch.dict(os.environ, {'MAST_AUTH_TOKEN': 'foo'}):
        panoptes._forward_contents({'foo': 'bar'}, 'mast')

    (requests.post).assert_called_once_with(
        timeout=5,
        url='https://mast-forwarder.zooniverse.org/',
        json={'foo': 'bar'},
        headers={'X-ASB-AUTH': 'foo'}
    )
