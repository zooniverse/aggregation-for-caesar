from importlib import import_module

from unittest.mock import MagicMock, PropertyMock, Mock, patch
from nose.tools import assert_equals, assert_raises, assert_count_equal
from panoptes_client import Panoptes, User
import requests

import os
from os import environ

environ.setdefault('AGGREGATION_PANOPTES_ID', 'TEST')
environ.setdefault('AGGREGATION_PANOPTES_SECRET', 'TEST')

panoptes = import_module('panoptes_aggregation.panoptes', __name__).panoptes_testing


def build_mock_user(**kwargs):
    mock_user = MagicMock()
    for key, value in kwargs.items():
        setattr(type(mock_user), key, PropertyMock(return_value=value, create=True))
    return mock_user


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
    assert_equals(panoptes.userify({}, {'foo': 'bar'}), '{"foo": "bar"}')
    assert_equals(panoptes.userify({'login': None}, {'foo': 'bar'}), '{"foo": "bar"}')
    assert_equals(panoptes.userify({}, {}), '{}')
    assert_equals(panoptes.userify({'login': None}, {}), '{}')

    # fills out object correctly
    (User.find) = Mock(return_value=build_mock_user(id=3, login="login 3"))
    assert_equals(panoptes.userify({'login': None}, {'user_id': 3}), '{"user_id": 3, "users": [{"id": 3, "login": "login 3"}]}')

    # forwards appropriately
    requests.post = MagicMock()
    assert_equals(panoptes.userify({'login': None, 'destination': 'mockable'}, {'user_id': 3}), '{"user_id": 3, "users": [{"id": 3, "login": "login 3"}]}')
    (requests.post).assert_called_once()


def test_unique():
    # removes duplicate elements
    assert_count_equal(panoptes._unique([]), [])
    assert_count_equal(panoptes._unique([3]), [3])
    assert_count_equal(panoptes._unique([3, 3]), [3])
    assert_count_equal(panoptes._unique([3, 3, 3]), [3])
    assert_count_equal(panoptes._unique([3, 4]), [3, 4])
    assert_count_equal(panoptes._unique([1, 1, 2, 3]), [1, 2, 3])
    assert_count_equal(panoptes._unique([1, 2, 3, 1]), [1, 2, 3])


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


def test_discover_fields():
    # can find simple list of properties
    assert_count_equal(panoptes._discover_fields({}), [])
    assert_count_equal(panoptes._discover_fields({'f1': 'v1'}), ['f1'])
    assert_count_equal(panoptes._discover_fields({'f1': 'v1', 'f2': 'v2'}), ['f1', 'f2'])
    assert_count_equal(panoptes._discover_fields({'f1': 'v1', 'destination': 'd1', 'f2': 'v2'}), ['f1', 'f2'])

    # ignores known fields
    assert_count_equal(panoptes._discover_fields({'destination': 'v1'}), [])
    assert_count_equal(panoptes._discover_fields({'destination': 'v1', 'f2': 'v2'}), ['f2'])


def test_build_user_hash():
    mock_user = build_mock_user(id=1, login='login', display_name='display_name')

    # fetches the specified properties and puts them in a hash
    assert_equals(panoptes._build_user_hash(mock_user, []), {'id': 1})
    assert_equals(panoptes._build_user_hash(mock_user, ['login']), {'id': 1, 'login': 'login'})
    assert_equals(panoptes._build_user_hash(mock_user, ['display_name']), {'id': 1, 'display_name': 'display_name'})
    assert_equals(panoptes._build_user_hash(mock_user, ['login', 'display_name']), {'id': 1, 'login': 'login', 'display_name': 'display_name'})


def test_retrieve_user():
    mock_user1 = build_mock_user(id=1, login='login', display_name='display_name')
    mock_user2 = build_mock_user(id=2, login='login', display_name='display_name')

    # make this a no-op
    Panoptes.connect = Mock()

    # finds user by calling API
    User.find = Mock(return_value=mock_user1)
    found_user = panoptes._retrieve_user(1)
    assert_equals(found_user, mock_user1)
    assert_equals(found_user.id, 1)
    (User.find).assert_called_once_with(1)

    # uses cached user object when possible instead of finding it again
    User.find = Mock(return_value=mock_user2)
    found_user = panoptes._retrieve_user(1)
    assert_equals(found_user, mock_user1)
    assert_equals(found_user.id, 1)
    (User.find).assert_not_called()


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


def user_find_side_effect(*args, **_):
    user_id = args[0]
    return build_mock_user(id=user_id, login='login {0}'.format(user_id), display_name='display_name {0}'.format(user_id))


def test_stuff_object():
    User.find = MagicMock(side_effect=user_find_side_effect)

    # doesn't crash on an empty object
    assert_equals(panoptes._stuff_object({}, []), {})
    assert_equals(panoptes._stuff_object({}, ['login']), {})

    # maintains existing properties
    assert_equals(panoptes._stuff_object({'foo': 'bar'}, ['login']), {'foo': 'bar'})
    assert_equals(panoptes._stuff_object({'foo': 'bar'}, []), {'foo': 'bar'})

    # builds a user even if no fields are requested
    assert_equals(panoptes._stuff_object({'user_id': 3}, []), {'user_id': 3, 'users': [{'id': 3}]})

    # adds requested fields
    assert_equals(panoptes._stuff_object({'user_id': 3}, ['login']), {'user_id': 3, 'users': [{'id': 3, 'login': 'login 3'}]})
    assert_equals(panoptes._stuff_object({'user_id': 3}, ['display_name']), {'user_id': 3, 'users': [{'id': 3, 'display_name': 'display_name 3'}]})
    assert_equals(panoptes._stuff_object({'user_id': 3}, ['login', 'display_name']), {'user_id': 3, 'users': [{'id': 3, 'display_name': 'display_name 3', 'login': 'login 3'}]})

    # finds fields in nested objects
    assert_equals(panoptes._stuff_object({'foo': {'user_id': 3}}, ['login', 'display_name']), {'foo': {'user_id': 3, 'users': [{'id': 3, 'display_name': 'display_name 3', 'login': 'login 3'}]}})

    # fetches multiple users if user_ids
    assert_equals(panoptes._stuff_object({'user_ids': [3, 4]}, []), {'user_ids': [3, 4], 'users': [{'id': 3}, {'id': 4}]})

    # handles null user ids
    assert_equals(panoptes._stuff_object({'user_ids': [3, None]}, []), {'user_ids': [3, None], 'users': [{'id': 3}]})

    # finds fields at multiple levels
    assert_equals(panoptes._stuff_object({'foo': {'user_id': 3}, 'user_id': 4}, []), {'foo': {'user_id': 3, 'users': [{'id': 3}]}, 'user_id': 4, 'users': [{'id': 4}]})


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
    (requests.post).assert_called_once_with(url='https://demo1580318.mockable.io/mast', json={'foo': 'bar'})

    requests.post = MagicMock()
    with patch.dict(os.environ, {'MAST_AUTH_TOKEN': 'foo'}):
        panoptes._forward_contents({'foo': 'bar'}, 'mast')

    (requests.post).assert_called_once_with(
        url='https://mast-forwarder.zooniverse.org/',
        json={'foo': 'bar'},
        headers={'X-ASB-AUTH': 'foo'}
    )
