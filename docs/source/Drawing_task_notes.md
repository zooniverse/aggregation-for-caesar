# Drawing task code architecture notes

Drawing tasks are one of the more complex task types on the Zooniverse.  As a result the aggregation code around these tasks has many moving parts.  These notes are designed to walk through the lifecycle of a drawing task's extraction and reduction and provide documentation around what parts of the code handel each one.


## General structure of a drawing task

A single drawing `task` is made up of a series drawing `tool`s.  These tools are the different shapes that a research team would like to allow the volunteers to be able to use.  Each `tool` can optionally have a `subtask`, this is a follow up `task` that a volunteer will be shown to add additional information about the shapes they draw (this is typically a question `task`).

The exact way the `classification` is structured in a project's data export is dependent on what frontend version the project whs built with (see below).  The frontend version is encoded in the `metadata.classifier_version` value inside the `classification` object.

Note: if the `metadata.classifier_version` key does not exist the `classification` version is `"1.0"`.  This key did not exist until the frontend rewrite that introduced version `"2.0"`.


## Frontend versions (PFE vs FEM)

Since the project builder came online in late 2014, the Zooniverse frontend has had two distinct versions.  Each version structures their `classification`s (especially the drawing `classification`s) in different ways.  This means that the aggregation code must be able to detect both flavors of `classification` and use the appropriate code for each.

### PFE

The first frontend what called the "Panoptes front-end" or PFE for short.  To illustrate the `classification` structure we will use a rectangle drawing task with two question subtasks as an example.

```json
{"annotations": [
    {
        "task": "T0",
        "value": [
            {
                "tool": 0,
                "frame": 0,
                "x": 0,
                "y": 0,
                "width": 5,
                "height": 10,
                "details": [
                    {"value": 0},
                    {"value": 1}
                ]
            },
            {
                "tool": 0,
                "frame": 0,
                "x": 100,
                "y": 105,
                "width": 50,
                "height": 100,
                "details": [
                    {"value": 1},
                    {"value": 2}
                ]
            },
            {
                "tool": 1,
                "frame": 0,
                "x": 500,
                "y": 500,
                "width": 10,
                "height": 20,
                "details": []
            }
        ]
    }
]}
```

Within the `classification` JSON is the `annotations` key, this contains a list `task`s, in the above example there is only one task `T0`.  Within the `task` object is the `value` key, this has all the information about each shape drawn for the associated `task`.  Above there are three rectangles drawn for task `T0`.  Each item of the `value` list contains a `tool` id that maps to what tool within the drawing task was use do draw the shape, a `frame` id that maps to what frame of the subject the drawing was made on, `details` that contains a list of the `subtask` classifications, and specific parameters that are based what shape is being drawn (`x`, `y`, `with`, and `height` in the case of the rectangle above).

A full list of each parameter for each shape tool for PFE classifications is stored in the `panoptes_aggregation.shape_tools.SHAPE_LUT` look up table.  For typical shapes, (e.g. circle, rectangle, point) these are the SVG parameters for the shapes.

### FEM

In 2026 the front-end monorepo (FEM) became the default for the Zooniverse.  During this update several things change to make the drawing annotation's data structure easier for aggregation to parse (among other improvements).  Below shows the same classification from above in FEM format.

```json
{"annotations": [
    {
        "task": "T0",
        "taskType": "drawing",
        "value": [
            {
                "toolIndex": 0,
                "toolType": "rectangle",
                "frame": 0,
                "x_center": 2.5,
                "y_center": 5,
                "width": 5,
                "height": 10,
                "details": [
                    {"task": "T0.0.0"},
                    {"task": "T0.0.1"}
                ]
            },
            {
                "toolIndex": 0,
                "toolType": "rectangle",
                "frame": 0,
                "x_center": 125,
                "y_center": 155,
                "width": 50,
                "height": 100,
                "details": [
                    {"task": "T0.0.0"},
                    {"task": "T0.0.1"}
                ]
            },
            {
                "toolIndex": 1,
                "toolType": "rectangle",
                "frame": 0,
                "x_center": 505,
                "y_center": 510,
                "width": 10,
                "height": 20,
                "details": []
            }
        ]
    }, {
        "task": "T0.0.0",
        "taskType": "single",
        "markIndex": 0,
        "value": 0
    }, {
        "task": "T0.0.0",
        "taskType": "single",
        "markIndex": 1,
        "value": 1
    }, {
        "task": "T0.0.1",
        "taskType": "single",
        "markIndex": 0,
        "value": 1
    }, {
        "task": "T0.0.1",
        "taskType": "single",
        "markIndex": 1,
        "value": 2
    }
], "metadata": {
    "classifier_version": "2.0"
}}
```

There are several differences that stand out:
- `metadata.classifier_version` is set to `"2.0"`
- `subtask` annotations sit at the top level of the `annotations` data structure with `markIndex` used to map it back to the associated drawn mark
- `tool` became `toolIndex`
- `toolType` and `taskType` are stored directly on the classification
- `details` stores the task key name rather than the full subtask classification
- The parameters used for each drawing tool have been adjusted to be more useful for data clustering (e.g. storing the centers of rectangles rather then upper left corner)

A full list of each parameter for each FEM shape tool is stored in the `panoptes_aggregation.shape_tools.SHAPE_LUT_FEM` look up table.

## Extraction process

The drawing extractors use three common wrappers
- `@subtask_wrapper`: provides code to extract the subtasks. This must be applied to the extractor *first* (decorator at the bottom of the stack) so that `markIndex` is applied correctly for FEM classifications.  This wrapper is also responsible for adding the classifier version to the extract if it is v2.0 or higher (this will inform the reducer later on what version of the shapes to use).
- `@tool_wrapper`: provides code for filtering the `annotations` list to only include classifications from a specified drawing tool index.  This wrapper will correctly track "markIndex" if a tool is filtered out.  Subtasks are not filtered by this wrapper, it is assumed the details mapping provided as a keyword has already been filtered to the specified tool index(s).
- `@extractor_wrapper`: provides code common to all extractors that detects if an extractor is being called in either "offline" or "online" mode and grabs the augments and keywords from the appropriate place before calling the extractor function.  This is also where the "pluckfield" extractor is called if its keywords are set.  Must be applied to the extractor *last* (decorator at the top of the stack).

Note: The above wrappers are all in the `panoptes_aggregation.extractors` subfolder.

To extract subtasks a mapping needs to be provided as a keyword that identifies what extractor should be used.  This mapping can be provide in one of two ways, the first was originally developed for PFE and the second was developed for FEM.  As one workflow can potentially have *both* PFE and FEM classifications, the code will automatically convert this mapping between its two styles as needed inside the `subtask_wrapper`.  As a result *either* style can be used without issue regardless of what version classification is passed in. 

### details mapping v1

```python
details = {
    'T0_tool0': ['question_extractor', 'question_extractor']
}
```

This is a python dictionary with the keys in the format `T<task number>_tool<tool index>` and the value being a `list` of extractors, one for each subtask of the drawing tool.  Any subtasks that should not be extracted can put the value `None` as an element of the list.

### details mapping v2

```python
details = {
    'T0_toolIndex0_subtask0': 'question_extractor',
    'T0_toolIndex0_subtask1': 'question_extractor'
}
```

This is a python dictionary with the keys in the format `T<task number>_toolIndex<tool index>_subtask<subtask index>` and the value being the name of the extractor.  Any subtasks that should not be extracted can put `None` as the value.

## Extraction output

Next let's look at the output of the a typical shape extractor from our example above.  This output will look different depending on the classifier version specified on the classification object.

### PFE

```json
{
    "frame0": {
        "T0_tool0_x": [0, 100],
        "T0_tool0_y": [0, 105],
        "T0_tool0_width": [5, 50],
        "T0_tool0_height": [10, 100],
        "T0_tool0_details": [
            [{"0": 1}, {"1": 1}],
            [{"1": 1}, {"2": 1}]
        ],
        "T0_tool1_x": [500],
        "T0_tool1_y": [500],
        "T0_tool1_width": [10],
        "T0_tool1_height": [20]
    }
}
```

The various shape parameters have been combined into lists of values grouped by the task ID and the tool index.  The subtasks are grouped as a list of lists, with each inner list contains the extracts for *each* subtask for a single classification, and the outer list keeping them in the same order as the lists of the other parameters.  Finally the tools and subtasks are all grouped by the subject frame index (if a subject has no `frame` value it defaults to `0`).

Note: the question extractor provides a "counter" mapping that says how many times a particular answer is given.  The key is the answer index, the value is always `1` for extraction.  This format make the reduction easier.

### FEM

```json
{
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_x_center": [2.5, 125],
        "T0_toolIndex0_y_center": [5, 155],
        "T0_toolIndex0_width": [5, 50],
        "T0_toolIndex0_height": [10, 100],
        "T0_toolIndex0_subtask0": [{"0": 1}, {"1": 1}],
        "T0_toolIndex0_subtask1": [{"1": 1}, {"2": 1}],
        "T0_toolIndex1_x_center": [505],
        "T0_toolIndex1_y_center": [510],
        "T0_toolIndex1_width": [10],
        "T0_toolIndex1_height": [20],
    }
}
```

The difference to before are the addition of `"classifier_version": "2.0"` to indicate what version the extract shape is takeing, and flattening the outer-most list of the subtasks extracts.

## Reduction process

The reduction process of drawing tasks follows these steps:
1. process the data into a more convenient data format for clustering
2. identify clusters in the drawn shapes
3. reduce any subtasks *within* each identified cluster
4. (optional) identified clusters are converted back in to FEM annotations so the front-end can display them to the next volunteer

As before some of these steps are applied using python decorators.
- `@subtask_wrapper`: provides code to reduce the subtasks based on the results of the clustering code. This must be applied to the reducer *first* (decorator at the bottom of the stack).  This wrapper is also responsible for adding the classifier version to the reduction if it is v2.0 or higher.
- `@collab_wrapper`: provides code to pass back the identified clusters to the Zooniverse front-end in a way that will show them to the next volunteer to see the subject.  See [Collaborative workflow](https://aggregation-caesar.zooniverse.org/docs/Collaborative%20workflow.html) for more details on setup.
- `@reducer_wrapper`: provides code common to all reducers that detects if an reducer is being called in either "offline" or "online" mode and grabs the augments and keywords from the appropriate place, apply the data processing function, and call the reduction function on the result.  Must be applied to the reducer *last* (decorator at the top of the stack).

Note: The above wrappers are all in the `panoptes_aggregation.reducers` subfolder.

### Details mapping

The format for passing in the subtask mapping to reducers is an identical format to the mapping used for extractors:

```python
details = {
    'T0_tool0': ['question_reducer', 'question_reducer']
}
```

or 

```python
details = {
    'T0_toolIndex0_subtask0': 'question_reducer',
    'T0_toolIndex0_subtask1': 'question_reducer'
}
```

Either format will work regardless of the classifier version.


## Reducer output

The first step of the reduction process is clustering the drawn shapes together, there are various algorithms for doing this that are covered in more detail in the [How Clustering Works](https://aggregation-caesar.zooniverse.org/How_Clustering_Works.html) notes.  For these notes it does not matter how the clustering is done as they all produce similar output structures.

### PFE

We will assume we have two v1.0 extracts we would like to reduce:

```json
[{
    "frame0": {
        "T0_tool0_x": [0, 100],
        "T0_tool0_y": [0, 105],
        "T0_tool0_width": [5, 50],
        "T0_tool0_height": [10, 100],
        "T0_tool0_details": [
            [{"0": 1}, {"1": 1}],
            [{"1": 1}, {"2": 1}]
        ],
        "T0_tool1_x": [500],
        "T0_tool1_y": [500],
        "T0_tool1_width": [10],
        "T0_tool1_height": [20]
    }
}, {
    "frame0": {
        "T0_tool0_x": [0, 100],
        "T0_tool0_y": [0, 105],
        "T0_tool0_width": [5, 50],
        "T0_tool0_height": [10, 100],
        "T0_tool0_details": [
            [{"1": 1}, {"1": 1}],
            [{"0": 1}, {"2": 1}]
        ]
    }
}]
```

All of the shape clustering reducers use the same `process_data` function, this takes in the extract and rearranges the parameters into a list of tuples, one item per drawn shape, sorted by frame, task, and tool.  This also tracks some metadata that is passed into the clustering code.

The processed data from the above input would be:

```python
{
    'shape': 'rectangle',
    'symmetric': False,
    'classifier_version': '1.0',
    'n_classifications': 2,
    'frame0': {
        'T0_tool0': [
            (0, 0, 5, 10),
            (100, 105, 50, 100),
            (0, 0, 5, 10),
            (100, 105, 50, 100),
        ],
        'T0_tool1': [
            (500, 500, 10, 20)
        ]
    }
}
```

Note: this output is only passed around inside the python code, so it does not need to follow JSON syntax.

We can see that the `classifier_version` is passed along with the `shape`, `n_classifications`, and `symmetric` keywords (provided as inputs to the reducer function and collaboration wrapper).  At this stage none of the subtask information is being passed into the reducer as it will be processed *after* the clustering is finished.

After clustering alone the output will look like:

```json
{
    "frame0": {
        "T0_tool0_rectangle_x": [0, 100, 0, 100],
        "T0_tool0_rectangle_y": [0, 105, 0, 105],
        "T0_tool0_rectangle_width": [5, 50, 5, 50],
        "T0_tool0_rectangle_height": [10, 100, 10, 100],
        "T0_tool0_cluster_labels": [0, 1, 0, 1],

        "T0_tool0_clusters_count": [2, 2],
        "T0_tool0_clusters_x": [0, 100],
        "T0_tool0_clusters_y": [0, 105],
        "T0_tool0_clusters_width": [5, 50],
        "T0_tool0_clusters_height": [10, 100],

        "T0_tool1_rectangle_x": [500],
        "T0_tool1_rectangle_y": [500],
        "T0_tool1_rectangle_width": [10],
        "T0_tool1_rectangle_height": [20],
        "T0_tool1_cluster_labels": [-1],
    }
}
```

This data structure stores the original extracts as a list for each parameter along side the labels saying what cluster those points belong to.  This is provided here because the order the extractions appear are not guaranteed to be the same when run in only mode through Caesar.  Any points that are marked as outliers and not belonging to a cluster are given a label of `-1` (`T0_tool1` in the example above).  For any clusters that are found a count for the number of shape in the clusters is provided along side the average values for the parameters within the cluster.

With the clusters defined the `subtask_wrapper` can now run the reducers for *each cluster found* and append it to the output.

```json
{
    "frame0": {
        "T0_tool0_rectangle_x": [0, 100, 0, 100],
        "T0_tool0_rectangle_y": [0, 105, 0, 105],
        "T0_tool0_rectangle_width": [5, 50, 5, 50],
        "T0_tool0_rectangle_height": [10, 100, 10, 100],
        "T0_tool0_cluster_labels": [0, 1, 0, 1],

        "T0_tool0_details": [
            [{"0": 1}, {"1": 1}],
            [{"1": 1}, {"2": 1}],
            [{"1": 1}, {"1": 1}],
            [{"0": 1}, {"2": 1}]
        ],

        "T0_tool0_clusters_count": [2, 2],
        "T0_tool0_clusters_x": [0, 100],
        "T0_tool0_clusters_y": [0, 105],
        "T0_tool0_clusters_width": [5, 50],
        "T0_tool0_clusters_height": [10, 100],

        "T0_tool0_clusters_details": [
            [{"0": 1, "1": 1}, {"1": 2}],
            [{"0": 1, "1": 1}, {"2": 2}]
        ],

        "T0_tool1_rectangle_x": [500],
        "T0_tool1_rectangle_y": [500],
        "T0_tool1_rectangle_width": [10],
        "T0_tool1_rectangle_height": [20],
        "T0_tool1_cluster_labels": [-1],
    }
}
```

The direct extracts are provided as a list-of-lists (`T0_tool0_details`) and the reductions within each cluster are provided as a list-of-lists  (`T0_tool0_clusters_details`).

### FEM

For the next example we will assume we have the same two extracts but this time formatted as v2.0:

```json
[{
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_x_center": [2.5, 125],
        "T0_toolIndex0_y_center": [5, 155],
        "T0_toolIndex0_width": [5, 50],
        "T0_toolIndex0_height": [10, 100],
        "T0_toolIndex0_subtask0": [{"0": 1}, {"1": 1}],
        "T0_toolIndex0_subtask1": [{"1": 1}, {"2": 1}],
        "T0_toolIndex1_x_center": [505],
        "T0_toolIndex1_y_center": [510],
        "T0_toolIndex1_width": [10],
        "T0_toolIndex1_height": [20]
    }
}, {
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_x_center": [2.5, 125],
        "T0_toolIndex0_y_center": [5, 155],
        "T0_toolIndex0_width": [5, 50],
        "T0_toolIndex0_height": [10, 100],
        "T0_toolIndex0_subtask0": [{"1": 1}, {"0": 1}],
        "T0_toolIndex0_subtask1": [{"1": 1}, {"2": 1}],
    }
}]
```

The processed data would be:

```python
{
    'shape': 'rectangle',
    'symmetric': False,
    'classifier_version': '2.0',
    'n_classifications': 2,
    'frame0': {
        'T0_toolIndex0': [
            (2.5, 5, 5, 10),
            (125, 155, 50, 100),
            (2.5, 5, 5, 10),
            (125, 155, 50, 100),
        ],
        'T0_toolIndex1': [
            (505, 510, 10, 20)
        ]
    }
}
```

The clustering before the subtask wrapper:

```json
{
    "frame0": {
        "T0_toolIndex0_rectangle_x_center": [2.5, 125, 2.5, 125],
        "T0_toolIndex0_rectangle_y_center": [5, 155, 5, 155],
        "T0_toolIndex0_rectangle_width": [5, 50, 5, 50],
        "T0_toolIndex0_rectangle_height": [10, 100, 10, 100],
        "T0_toolIndex0_cluster_labels": [0, 1, 0, 1],

        "T0_toolIndex0_clusters_count": [2, 2],
        "T0_toolIndex0_clusters_x_center": [2.5, 125],
        "T0_toolIndex0_clusters_y_center": [5, 155],
        "T0_toolIndex0_clusters_width": [5, 50],
        "T0_toolIndex0_clusters_height": [10, 100],

        "T0_toolIndex1_rectangle_x_center": [505],
        "T0_toolIndex1_rectangle_y_center": [510],
        "T0_toolIndex1_rectangle_width": [10],
        "T0_toolIndex1_rectangle_height": [20],
        "T0_toolIndex1_cluster_labels": [-1],
    }
}
```

And with the subtask added in:

```json
{
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_rectangle_x_center": [2.5, 125, 2.5, 125],
        "T0_toolIndex0_rectangle_y_center": [5, 155, 5, 155],
        "T0_toolIndex0_rectangle_width": [5, 50, 5, 50],
        "T0_toolIndex0_rectangle_height": [10, 100, 10, 100],
        "T0_toolIndex0_cluster_labels": [0, 1, 0, 1],

        "T0_toolIndex0_subtask0": [
            {"0": 1},
            {"1": 1},
            {"1": 1},
            {"0": 1},
        ],
        "T0_toolIndex0_subtask1": [
            {"1": 1},
            {"2": 1},
            {"1": 1},
            {"2": 1}
        ],

        "T0_toolIndex0_clusters_count": [2, 2],
        "T0_toolIndex0_clusters_x_center": [2.5, 125],
        "T0_toolIndex0_clusters_y_center": [5, 155],
        "T0_toolIndex0_clusters_width": [5, 50],
        "T0_toolIndex0_clusters_height": [10, 100],

        "T0_toolIndex0_subtask0_clusters": [
            {"0": 1, "1": 1},
            {"0": 1, "1": 1}
        ],
        "T0_toolIndex0_subtask1_clusters": [
            {"1": 2},
            {"2": 2}
        ],

        "T0_toolIndex1_rectangle_x_center": [505],
        "T0_toolIndex1_rectangle_y_center": [510],
        "T0_toolIndex1_rectangle_width": [10],
        "T0_toolIndex1_rectangle_height": [20],
        "T0_toolIndex1_cluster_labels": [-1],
    }
}
```

As with the extractor subtask wrapper, the main difference between the v1.0 and v2.0 outputs is a flattening of the list-of-lists.

### Mixed PFE and FEM

The final case we need to look at is when there is a mix of classifier versions 1.0 and 2.0 being passed into the reducer.  Internally the aggregation code will convert the 1.0 extracts to 2.0 extracts and proceed with the 2.0 code from that point.

Let's look at the input:

```json
[{
    "frame0": {
        "T0_tool0_x": [0, 100],
        "T0_tool0_y": [0, 105],
        "T0_tool0_width": [5, 50],
        "T0_tool0_height": [10, 100],
        "T0_tool0_details": [
            [{"0": 1}, {"1": 1}],
            [{"1": 1}, {"2": 1}]
        ],
        "T0_tool1_x": [500],
        "T0_tool1_y": [500],
        "T0_tool1_width": [10],
        "T0_tool1_height": [20]
    }
}, {
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_x_center": [2.5, 125],
        "T0_toolIndex0_y_center": [5, 155],
        "T0_toolIndex0_width": [5, 50],
        "T0_toolIndex0_height": [10, 100],
        "T0_toolIndex0_subtask0": [{"1": 1}, {"0": 1}],
        "T0_toolIndex0_subtask1": [{"1": 1}, {"2": 1}],
    }
}]
```

The process data function will detect there is a mix of classifier versions and will convert the parameter of the v1.0 shapes to those of v2.0 (e.g. in this case `x` -> `x_center` and `y`->`y_center`).  The conversion code is located in `panoptes_aggregation.reducers.shape_normalization.SHAPE_VERSION_CONVERT`.

```python
{
    'shape': 'rectangle',
    'symmetric': False,
    'classifier_version': '2.0',
    'n_classifications': 2,
    'frame0': {
        'T0_toolIndex0': [
            (2.5, 5, 5, 10),
            (125, 155, 50, 100),
            (2.5, 5, 5, 10),
            (125, 155, 50, 100),
        ],
        'T0_toolIndex1': [
            (505, 510, 10, 20)
        ]
    }
}
```

From this point the processed data looks identical to when all extracts were v2.0, this means the clustering result is also identical before the subtask wrapper is called.  Internally the subtask wrapper will convert the v1.0 `T0_tool0_details` into the v2.0 flattened format before running.  This conversion is done by the `panoptes_aggregation.details_convert.details_extract_flatten` function.  This conversion means that the results will look identical to the FEM case above:

```json
{
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_rectangle_x_center": [2.5, 125, 2.5, 125],
        "T0_toolIndex0_rectangle_y_center": [5, 155, 5, 155],
        "T0_toolIndex0_rectangle_width": [5, 50, 5, 50],
        "T0_toolIndex0_rectangle_height": [10, 100, 10, 100],
        "T0_toolIndex0_cluster_labels": [0, 1, 0, 1],

        "T0_toolIndex0_subtask0": [
            {"0": 1},
            {"1": 1},
            {"1": 1},
            {"0": 1},
        ],
        "T0_toolIndex0_subtask1": [
            {"1": 1},
            {"2": 1},
            {"1": 1},
            {"2": 1}
        ],

        "T0_toolIndex0_clusters_count": [2, 2],
        "T0_toolIndex0_clusters_x_center": [2.5, 125],
        "T0_toolIndex0_clusters_y_center": [5, 155],
        "T0_toolIndex0_clusters_width": [5, 50],
        "T0_toolIndex0_clusters_height": [10, 100],

        "T0_toolIndex0_subtask0_clusters": [
            {"0": 1, "1": 1},
            {"0": 1, "1": 1}
        ],
        "T0_toolIndex0_subtask1_clusters": [
            {"1": 2},
            {"2": 2}
        ],

        "T0_toolIndex1_rectangle_x_center": [505],
        "T0_toolIndex1_rectangle_y_center": [510],
        "T0_toolIndex1_rectangle_width": [10],
        "T0_toolIndex1_rectangle_height": [20],
        "T0_toolIndex1_cluster_labels": [-1],
    }
}
```

## use_v1_keys=True

The process data function has the optional keyword `use_v1_keys`, when set to `True` it will replace instances of `toolIndex` with `tool` in the output for all non-subtask related outputs.  This is provided to aid projects migrating from PFE to FEM and don't want to adjust their data processing pipeline (e.g. a Caesar rule).  The subtask keys are not changed as there does not seem to be any need for that.  As this is a hold over for projects during the transition period it is expected the need for this keyword will be very limited in scope.

Note: this will only change the label, it will *not* convert to the previous parameterization.  So `T0_toolIndex1_rectangle_x_center` will become `T0_tool1_rectangle_x_center` *not* `T0_tool1_rectangle_x` in the above example.  For shapes that did not change their parameterization (e.g. circle, line, and point) it will be identical to the previous v1.0 output and the ellipse tool will only be different by the sign of the angle.  Again, this is due to the expected limited use case for this keyword.

## Collaborative drawing tasks

With the transcription task the Zooniverse added the ability to create collaborative workflows.  These are workflows where the front-end is able to query Caesar for a subject's current reduction and provide this as a starting point for the next volunteer.  This feature can now be turned on for any of the FEM drawing tasks.  To work, the reduction needs to add a `"data"` key to the JSON output that converts the consensus shapes (e.g. all the identified clusters) back into a FEM classification (sort of an "un-extractor").  This re-formatting is handled by the `collab_wrapper` when the `collab=True` keyword is set.

This wrapper adds several new keywords that can be passed into the drawing reducers:
- `collab`: When set to `True` the identified clusters are turned back into FEM annotations.  These will be shown as a starting point for the next volunteer who sees the subject.
- `step_key`: On FEM workflows have a concept of "steps" that can made up of one or several "tasks".  If your drawing task is the first question of your workflow this will be "S0".
- `task_index`: If a step is made up of several tasks (e.g. via the combo task), this value indicates what the index of the drawing task is.  This will typically be `0`.
- `min_threshold`: The ratio of the number of volunteers who have identified a cluster and the total number of volunteers who have classified the subject is the "threshold" value for the cluster.  Only clusters that have a threshold value above this minimum will be shown to the next volunteer.  Defaults to `0` (e.g. all clusters always shown).

In the above example if `collab=True` the result would be:

```json
{
    "classifier_version": "2.0",
    "frame0": {
        "T0_toolIndex0_rectangle_x_center": [2.5, 125, 2.5, 125],
        "T0_toolIndex0_rectangle_y_center": [5, 155, 5, 155],
        "T0_toolIndex0_rectangle_width": [5, 50, 5, 50],
        "T0_toolIndex0_rectangle_height": [10, 100, 10, 100],
        "T0_toolIndex0_cluster_labels": [0, 1, 0, 1],

        "T0_toolIndex0_clusters_count": [2, 2],
        "T0_toolIndex0_clusters_x_center": [2.5, 125],
        "T0_toolIndex0_clusters_y_center": [5, 155],
        "T0_toolIndex0_clusters_width": [5, 50],
        "T0_toolIndex0_clusters_height": [10, 100],

        "T0_toolIndex1_rectangle_x_center": [505],
        "T0_toolIndex1_rectangle_y_center": [510],
        "T0_toolIndex1_rectangle_width": [10],
        "T0_toolIndex1_rectangle_height": [20],
        "T0_toolIndex1_cluster_labels": [-1],
    },

    "data": [
        {
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "drawing",
            "toolIndex": 0,
            "frame": 0,
            "markId": "collab_frame0_T0_toolIndex0_0",
            "toolType": "rectangle",
            "x_center": 2.5,
            "y_center": 5,
            "width": 5,
            "height": 10
        },
        {
            "stepKey": "S0",
            "taskIndex": 0,
            "taskKey": "T0",
            "taskType": "drawing",
            "toolIndex": 0,
            "frame": 0,
            "markId": "collab_frame0_T0_toolIndex0_1",
            "toolType": "rectangle",
            "x_center": 125,
            "y_center": 155,
            "width": 50,
            "height": 100
        }
    ]
}
```

The next time a volunteer viewed the subject above it would be populated with two rectangles drawn with the first tool of the drawing task.

Note: The `markID` must be unique for each item in the returned list. 

### Limitations

There are a few limitations to how collaborative drawing tasks work:
- `CaesarDataFetching` must be turned on for the workflow by a Zooniverse admin and the project team must activate the "Enable Caesar Data Fetching" checkbox in the workflow settings.
- The Caesar reducer must have the key `machineLearnt` and must have "Pubic Extracts" and "Public Reductions" turned on.
- All drawing tools must be the same shape and be part of the same drawing task.  This comes down to restrictions in how panoptes_aggregation can only reduce one shape at a time and how `CaesarDataFetching` can only grab data from one reducer.
- No subtasks should be associated with the collaborative drawing task.  While this technically possible it would require any subtask reducers to calculate a valid consensus value.  This is something many of the reducer don't do (e.g. the question reducer gives counts for each answer) and is currently outside the scope of this feature.
