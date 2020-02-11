.. _gravity-spy:

Gravity Spy Notes
=================

Gravity Spy's leveling up and aggregation work as follows.

Confusion Matrix
----------------

After classifying on a gold standard subject a volunteer's
confusion matrix is estimated/updated. All gold standard subjects
have a machine learning (ML) label. This matrix has one row and one
column for each of the categories available to pick from in the
front-end (22 at the top level). The column indicates the value
the volunteer voted on and row indicates the value of the ML label.

As and example lets look at a case where there are only 5 categories
to pick from.

.. math::

    \text{CM} = \overbrace{\begin{bmatrix}
        5 & 1 & 1 & 0 & 0 \\
        2 & 4 & 1 & 0 & 0 \\
        1 & 0 & 6 & 0 & 1 \\
        0 & 2 & 0 & 6 & 2 \\
        0 & 1 & 2 & 3 & 3 \\
    \end{bmatrix}}^{
        \textstyle
        \text{Answer index}
    }\left.\rule{0cm}{1.2cm}\right\}\text{ML index}

What this looks like in the code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Within the `gravity_spy_user_reducer` store this is
structured as two nested dictionaries with the first key indicating
the column and the second key indicating the row (category labels will
be used as keys):

.. code-block:: python

    confusion_matrix = {
        '1': {'1': 5, '2': 2, '3': 1},
        '2': {'1': 1, '2': 4, '4': 2, '5': 1},
        '3': {'1': 1, '2': 1, '3': 6, '5': 2},
        '4': {'4': 6, '5': 3},
        '5': {'3': 1, '4': 2, '5': 3}
    }

Volunteer skill
---------------

To get the volunteer skill the columns of the CM need to be normalized so
they sum to 1 (i.e. divide each column by the number N of times a category
was voted for).

In this example:

.. math::

    \text{N} = \begin{bmatrix}
        8,
        8,
        10,
        9,
        6
    \end{bmatrix}

.. math::

    \frac{\text{CM}}{\text{N}} =
    \text{CM}_{\text{Norm}} = \begin{bmatrix}
        5/8 & 1/8  & 1/10 & 0   & 0   \\
        2/8 & 4/8  & 1/10 & 0   & 0   \\
        1/8 & 0    & 6/10 & 0   & 1/6 \\
        0   & 2/8 & 0     & 6/9 & 2/6 \\
        0   & 1/8  & 2/10 & 3/9 & 3/6 \\
    \end{bmatrix}

The diagonal of this normalized matrix gives how often the volunteer correctly
identifies each of the categories. Once all of these values pass a given
threshold (set in the reducer's configuration) the volunteer is promoted to
the next level.

.. math::

    \alpha = \text{diag}(\text{CM}_{\text{Norm}}) = \left[
        \frac{5}{8},
        \frac{4}{8},
        \frac{6}{10},
        \frac{6}{9},
        \frac{3}{6}
    \right]

In this example this volunteer will not be promoted to the next level since not
every value of :math:`\alpha` is above :math:`0.7`.

What this looks like in the code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`running_reducer/gravity_spy_user_reducer.py` returns `alpha`, `level_up`,
`max_workflow_id`, `max_level`, and `normalized_confusion_matrix` directly
on the reducer, and `max_level`, `column_normalization` (N above), and
`confusion_matrix` in the store. The `alpha` keys to check at each level and
the threshold they need to pass are set with `level_config` and `first_level`
key words. When a level up is triggered the `level_up` value will switch from
`False` to `True` and the `max_workflow_id` will indicate the ID for the new
workflow to unlock.

An example of the level_config is:

.. code-block:: python

    {
        'level_1': {
            'workflow_id': 1,
            'new_categories': [
                'BLIP',
                'WHISTLE'
            ],
            'threshold': 0.7,
            'next_level': 'level_2'
        },
        'level_2': {
            'workflow_id': 2
        }
    }

and in this case `first_level` would be set to `'level_1'`.

Retiring subjects
-----------------

When the volunteer above classifies a new subject the
:math:`\text{CM}_{\text{Norm}}` is used to determine how much
their vote contributes towards retirement.

Let's assume this volunteer voted for the 3rd category. Their
contribution will be the 3rd column:

.. math::

    \text{W}_i = \left[\frac{1}{10}, \frac{1}{10}, \frac{6}{10}, 0, \frac{2}{10} \right]

This is averaged with the contributions from the other volunteers
who voted on the subject and the ML score :math:`p^{ML}`

.. math::

    \text{W} = \frac{\sum_{i=1}^{n}{\text{W}_i} + p^{ML}}{n + 1}

When the maximum value of W passes the threshold (currently set
to 0.9) the image is retired. W is normalized so that all the
values in the vector sum to 1.

When the maximum value of :math:`\text{W}` passes the threshold
(e.g. 0.9) the image is retired.

What this looks like in the code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`running_reducer/gravity_spy_subject_reducer.py` returns `number_views`,
`none_of_the_above_count`, `category_weights` (W above), and
`max_category_weight`. The store has the two counts above and a
running sum `category_weights_sum`.

The subject retirement rule can use a combination of `number_views` and
`max_category_weight` (e.g. when `number_views >= 3` and
`max_category_weight > 0.9` retire the subject)

Moving subjects to the next level
---------------------------------

If three or more volunteers vote for "None of the above" the subject
is moved to the next level up.

What this looks like in the code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`running_reducer/gravity_spy_subject_reducer.py` returns
`none_of_the_above_count` to use for this rule (e.g.
when `none_of_the_above_count >= 3` move subject to the next level).

Other notes
-----------

A volunteer's classification is ignored if their CM column is all
zeros for the answer they have given (i.e. they have never voted
for a particular category on any gold standard subject). Additionally,
if they classify a subject as "none of the above" the `number_views`
counter is not incremented and the current `category_weights` is not
changed. This also means classifications from non-logged in volunteers
are ignored (although if you are not logged in you can not see past the
level 1 workflow so not that big a deal).

The ML weights count as 1 view (treated the same as any of the volunteers),
so until `number_views >= 2` it has not been classified by a volunteer with
a non-zero CM column.
