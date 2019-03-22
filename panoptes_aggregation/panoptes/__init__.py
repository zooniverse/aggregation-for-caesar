try:
    from .userify import userify
except ImportError:
    print('`panoptes_aggregation.panoptes.userfy` is only available in online mode `pip install panoptes_aggregation[online]`')

panoptes = {
  'userify': userify
}
