from typing import Any


def construct_filter_string(filters: dict[str, Any]) -> str:
    '''
    Construct a filtering string from a dictionary of filters
    that can be used in GQL queries to filter values.

    Args:
        filters: A dictionary in which keys are the fields to filter,
                 and values are the values to filter by.
    Returns:
        A filter string usable in GQL queries.
    '''
    prepped_filters = []
    for key, f in filters.items():
        filter = ''
        if type(f) is str:
            filter = f'{key}: "{f}"'
        elif type(f) is bool:
            # bool type must be lowercase
            filter = f'{key}: {str(f).lower()}'
        else:
            filter = f'{key}: {f}'
        prepped_filters.append(filter)
    return ', '.join(prepped_filters)
