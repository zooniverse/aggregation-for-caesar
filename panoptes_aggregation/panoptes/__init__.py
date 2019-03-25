from importlib import import_module

try:
    from .userify import userify
    _userify = import_module('.userify', __name__)
except ImportError: # pragma: no cover
    print('`panoptes_aggregation.panoptes.userify` is only available in online mode `pip install panoptes_aggregation[online]`') # pragma: no cover

panoptes = {
  'userify': userify
}

panoptes_testing = _userify
