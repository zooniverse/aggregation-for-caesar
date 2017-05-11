def process_kwargs(kwargs, DEFAULTS={}):
    kwargs_out = {}
    for k, v in DEFAULTS.items():
        kwargs_out[k] = kwargs.get(k, **v)
    return kwargs_out
