from .tess_user_reducer import tess_user_reducer
from .tess_reducer_column import tess_reducer_column_rr
from .tess_gold_standard_reducer import tess_gold_standard_reducer_rr



running_reducers = {
    'tess_user_reducer': tess_user_reducer,
    'tess_reducer_column': tess_reducer_column_rr,
    'tess_gold_standard_reducer': tess_gold_standard_reducer_rr
}
