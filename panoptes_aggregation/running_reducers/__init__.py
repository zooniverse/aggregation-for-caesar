from .tess_user_reducer import tess_user_reducer
from .tess_gold_standard_reducer import tess_gold_standard_reducer_rr


running_reducers = {
    'tess_user_reducer': tess_user_reducer,
    'tess_gold_standard_reducer': tess_gold_standard_reducer_rr
}
