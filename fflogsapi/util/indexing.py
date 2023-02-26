from typing import Any


def itindex(dictionary: dict, indices: list[str]) -> Any:
    '''
    Index a `dictionary` iteratively by a list of `indices`.

    Args:
        `dictionary`: The dict to index.
        `indices`: A list of indices.
    '''
    result = None
    for idx in indices:
        if result is None:
            result = dictionary[idx]
        else:
            result = result[idx]
    return result
