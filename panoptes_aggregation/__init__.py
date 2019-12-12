import warnings
# uncomment this filter and run `nosetests -s` to makre all warnings print when running tests
# warnings.filterwarnings("always")
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")
from . import extractors
from . import reducers
from . import running_reducers
from . import scripts
from . import version
__version__ = version.__version__
