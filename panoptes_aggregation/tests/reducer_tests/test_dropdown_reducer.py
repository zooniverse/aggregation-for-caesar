from collections import Counter
from panoptes_aggregation.reducers.dropdown_reducer import process_data, dropdown_reducer
from .base_test_class import ReducerTest

extracted_data = [
    {
        'value': [
            {'option-1': 1},
            {'option-2': 1},
            {'None': 1}
        ]
    },
    {
        'value': [
            {'option-4': 1},
            {'option-2': 1},
            {'None': 1}
        ]
    },
    {
        'value': [
            {'option-1': 1},
            {'option-3': 1},
            {'option-5': 1}
        ]
    }
]

processed_data = [
    [
        Counter({'option-1': 1}),
        Counter({'option-2': 1}),
        Counter({'None': 1})
    ],
    [
        Counter({'option-4': 1}),
        Counter({'option-2': 1}),
        Counter({'None': 1})
    ],
    [
        Counter({'option-1': 1}),
        Counter({'option-3': 1}),
        Counter({'option-5': 1})
    ]
]

reduced_data = {
    'value': [
        {'option-1': 2, 'option-4': 1},
        {'option-2': 2, 'option-3': 1},
        {'None': 2, 'option-5': 1}
    ]
}

TestDropdownReducer = ReducerTest(
    dropdown_reducer,
    process_data,
    extracted_data,
    processed_data,
    reduced_data,
    'Test dropdown reducer',
    processed_type='list'
)
