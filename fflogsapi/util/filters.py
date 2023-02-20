from typing import Any, Dict


def construct_filter_string(filters: Dict[str, Any]) -> str:
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
