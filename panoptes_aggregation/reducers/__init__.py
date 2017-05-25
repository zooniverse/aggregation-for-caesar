from . import cluster_points
from .process_kwargs import process_kwargs

reducers = {
    'point_reducer': cluster_points.reducer_request
}
