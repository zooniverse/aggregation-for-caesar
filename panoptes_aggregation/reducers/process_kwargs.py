from werkzeug.datastructures import MultiDict


def process_kwargs(kwargs_in, DEFAULTS={}):
    kwargs = MultiDict(kwargs_in)
    kwargs_out = {}
    for k, v in DEFAULTS.items():
        kwargs_out[k] = kwargs.get(k, **v)
    return kwargs_out
