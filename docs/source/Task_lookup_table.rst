What extractor and reducer should be used?
==========================================

Here is a list of the Panoptes task types that are currently supported and what extractor and reducer should be used for each.

Basic task types
----------------

+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Task Type          | Extractor                                                            | Reducer                                                                               |
+====================+======================================================================+=======================================================================================+
| Single Question    | :mod:`panoptes_aggregation.extractors.question_extractor`            | :mod:`panoptes_aggregation.reducers.question_reducer`                                 |
+--------------------+                                                                      |                                                                                       |
| Multiple Question  |                                                                      |                                                                                       |
+--------------------+                                                                      |                                                                                       |
| Shortcut           |                                                                      |                                                                                       |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Dropdown           | :mod:`panoptes_aggregation.extractors.dropdown_extractor`            | :mod:`panoptes_aggregation.reducers.dropdown_reducer`                                 |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Slider             | :mod:`panoptes_aggregation.extractors.slider_extractor`              | :mod:`panoptes_aggregation.reducers.slider_reducer`                                   |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Survey             | :mod:`panoptes_aggregation.extractors.survey_extractor`              | :mod:`panoptes_aggregation.reducers.survey_reducer`                                   |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Point              | :mod:`panoptes_aggregation.extractors.point_extractor_by_frame`      | :mod:`panoptes_aggregation.reducers.point_reducer_dbscan` (includes cov information)  |
|                    |                                                                      +---------------------------------------------------------------------------------------+
|                    |                                                                      | :mod:`panoptes_aggregation.reducers.point_reducer_hdbscan` (includes cov information) |
|                    +----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
|                    | :mod:`panoptes_aggregation.extractors.shape_extractor`               | :mod:`panoptes_aggregation.reducers.shape_reducer_dbscan` (no cov infromation)        |
|                    |                                                                      +---------------------------------------------------------------------------------------+
|                    |                                                                      | :mod:`panoptes_aggregation.reducers.shape_reducer_hdbscan` (no cov infromation)       |
|                    +----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
|                    | :mod:`panoptes_aggregation.extractors.point_extractor` (depreciated) | :mod:`panoptes_aggregation.reducers.point_reducer` (depreciated)                      |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Rectangle          | :mod:`panoptes_aggregation.extractors.rectangle_extractor`           | :mod:`panoptes_aggregation.reducers.rectangle_reducer`                                |
|                    +----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
|                    | :mod:`panoptes_aggregation.extractors.shape_extractor`               | :mod:`panoptes_aggregation.reducers.shape_reducer_dbscan`                             |
|                    |                                                                      +---------------------------------------------------------------------------------------+
|                    |                                                                      | :mod:`panoptes_aggregation.reducers.shape_reducer_hdbscan`                            |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+
| Circle             | :mod:`panoptes_aggregation.extractors.shape_extractor`               | :mod:`panoptes_aggregation.reducers.shape_reducer_dbscan`                             |
+--------------------+                                                                      |                                                                                       |
| Column             |                                                                      |                                                                                       |
+--------------------+                                                                      |                                                                                       |
| Full Width Line    |                                                                      |                                                                                       |
+--------------------+                                                                      |                                                                                       |
| Full Height Line   |                                                                      |                                                                                       |
+--------------------+                                                                      +---------------------------------------------------------------------------------------+
| Line               |                                                                      | :mod:`panoptes_aggregation.reducers.shape_reducer_hdbscan`                            |
+--------------------+                                                                      |                                                                                       |
| Rotating Rectangle |                                                                      |                                                                                       |
+--------------------+                                                                      |                                                                                       |
| Triangle           |                                                                      |                                                                                       |
+--------------------+                                                                      |                                                                                       |
| Fan                |                                                                      |                                                                                       |
+--------------------+----------------------------------------------------------------------+---------------------------------------------------------------------------------------+

-----

Text transcription projects
---------------------------
These are extractors and reducers designed for specific text transcription projects.

+--------------------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------+
| Task Type                            | Extractor                                                       | Reducer                                                            |
+======================================+=================================================================+====================================================================+
| Shakespeare's World variant          | :mod:`panoptes_aggregation.extractors.sw_variant_extractor`     | :mod:`panoptes_aggregation.reducers.sw_variant_reducer`            |
+--------------------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------+
| Shakespeare's World/AnnoTate graphic | :mod:`panoptes_aggregation.extractors.sw_graphic_extractor`     | :mod:`panoptes_aggregation.reducers.rectangle_reducer`             |
+--------------------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------+
| Shakespeare's World/AnnoTate text    | :mod:`panoptes_aggregation.extractors.sw_extractor`             | :mod:`panoptes_aggregation.reducers.poly_line_text_reducer`        |
+--------------------------------------+-----------------------------------------------------------------+                                                                    |
| Line tool with text sub-task         | :mod:`panoptes_aggregation.extractors.line_text_extractor`      |                                                                    |
+--------------------------------------+-----------------------------------------------------------------+                                                                    |
| Polygon tool with text sub-task      | :mod:`panoptes_aggregation.extractors.poly_line_text_extractor` |                                                                    |
+--------------------------------------+-----------------------------------------------------------------+--------------------------------------------------------------------+

----

TESS project
------------
These reducers were designed for use with the TESS project to handle real-time user weighting of identified column tool clusters.  This process requires proper
`relevant_reduction` being set for each reducer and several extractors/reducers internal to Caesar.

+-----------------------------------+--------------------------------------------------------+----------------------------------------------------------------+
| Task Type                         | Extractor                                              | Reducer                                                        |
+===================================+========================================================+================================================================+
| TESS Column Tool                  | :mod:`panoptes_aggregation.extractors.shape_extractor` | :mod:`panoptes_aggregation.reducers.tess_reducer_column`       |
+-----------------------------------+--------------------------------------------------------+----------------------------------------------------------------+
| TESS Classification of GS subject | Caesar's `PluckFieldExtractor`                         | :mod:`panoptes_aggregation.running_reducers.tess_user_reducer` |
+-----------------------------------+--------------------------------------------------------+----------------------------------------------------------------+
