import warnings
# uncomment this filter and run `nosetests -s` to makre all warnings print when running tests
# warnings.filterwarnings("always")
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from .version import __version__


# work around until https://github.com/pypa/flit/pull/382 (or similar) is merged into flit
def within_flit():
    import traceback
    for frame in traceback.extract_stack():
        if frame.name == "get_docstring_and_version_via_import":
            return True
    return False


if not within_flit():
    from . import extractors
    from . import reducers
    from . import running_reducers
    from . import scripts
