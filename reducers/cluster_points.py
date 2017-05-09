import numpy as np
from sklearn.cluster import DBSCAN


def process_data(data):
    # this will take the extracted data dumps and format them into an
    # array that DBSCAN can use
    # data comes in as [{tool1_x: 1, tool1_y: 2, tool2_x: 3, tool2_y: 4}, {tool1_x: 1, tool1_y: 2}, ...]
    unique_tools = set(sum([[k.split('_')[0] for k in d.keys()] for d in data], []))
    data_by_tool = {}
    for tool in unique_tools:
        tool_loc = []
        for d in data:
            x_key = '{0}_x'.format(tool)
            y_key = '{0}_y'.format(tool)
            if (x_key in d) and (y_key in d):
                tool_loc.append([d[x_key], d[y_key]])
        data_by_tool[tool] = np.array(tool_loc)
    return data_by_tool


def cluster_points(data, esp=5, min_samples=3):
    data_by_tool = process_data(data)
    clusters = {}
    for tool, loc in data_by_tool.items():
        if loc.shape[0] > min_samples:
            db = DBSCAN(esp=esp, min_samples=min_samples).fit(X)
            for k in set(db.labels_):
                if k > -1:
                    idx = db.labels_ == k
                    # number of points in the cluster
                    clusters['{0}_cluster{1}_count'.format(tool, k)] = idx.sum()
                    # mean of the cluster
                    k_loc = loc[idx].mean(axis=0)
                    clusters['{0}_cluster{1}_x'.format(tool, k)] = k_loc[0]
                    clusters['{0}_cluster{1}_y'.format(tool, k)] = k_loc[1]
                    # cov matrix of the cluster
                    k_cov = np.cov(loc[idx].T)
                    clusters['{0}_cluster{1}_var_x'.format(tool, k)] = k_cov[0, 0]
                    clusters['{0}_cluster{1}_var_y'.format(tool, k)] = k_cov[1, 1]
                    clusters['{0}_cluster{1}_var_x_y'.format(tool, k)] = k_cov[0, 1]
    return clusters
