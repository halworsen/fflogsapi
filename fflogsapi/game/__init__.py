'''
Client extensions providing access to `gameData` in the v2 FF Logs API.
'''

from ..data import FFGrandCompany, FFJob
from .pages import (FFAbility, FFItem, FFLogsAbilityPage, FFLogsAbilityPaginationIterator,
                    FFLogsItemPage, FFLogsItemPaginationIterator, FFLogsMapPage,
                    FFLogsMapPaginationIterator, FFMap,)

__all__ = [
    # dataclasses.py
    'FFAbility',
    'FFItem',
    'FFJob',
    'FFGrandCompany',
    'FFMap',

    # pages.py
    'FFLogsAbilityPage',
    'FFLogsAbilityPaginationIterator',
    'FFLogsItemPage',
    'FFLogsItemPaginationIterator',
    'FFLogsMapPage',
    'FFLogsMapPaginationIterator',
]
