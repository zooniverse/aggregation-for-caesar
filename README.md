# python-reducers-for-caesar

This is a collection of external reducers written for [caesar](https://github.com/zooniverse/caesar).

## Build/run the app
To run a local version use:
```bash
./bin/build.sh
./bin/up.sh
```
and listen on `localhost:8000`.

## run tests
To run the tests use:
```bash
./bin/test.sh
```

## API
Clustering points:
  - endpoint: `/cluster_points/?eps=5&min_samples=3`
  - This uses [scikitlearn's DBSCAN](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html#sklearn.cluster.DBSCAN) to cluster the data points. (NOTE: `eps` is in "pixels")
  - URL args can be set for any of DBSCAN's keywords
  - response contains the number of cluster points, x and y position (in pixels) of the cluster center, and values of the covariance matrix for clustered data points for each tool and cluster:
    ```js
    {
      tool1_cluster0_count: 5,
      tool1_cluster0_x: 20,
      tool1_cluster0_y: 10,
      tool1_cluster0_var_x: 2,
      tool1_cluster0_var_y: 1.5,
      tool1_cluster0_var_x_y: 0.5,
      tool1_cluster1_x: 5,
      tool1_cluster1_y: 35,
      tool1_cluster1_var_x: 1.5,
      tool1_cluster1_var_y: 2,
      tool1_cluster1_var_x_y: -0.5,
      tool2_cluster0_...
    }
    ```
