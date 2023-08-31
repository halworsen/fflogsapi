'''
Client extensions providing access to `worldData` in the v2 FF Logs API.
'''

from .dataclasses import FFLogsPartition
from .encounter import FFLogsEncounter
from .expansion import FFLogsExpansion
from .pages import (FFLogsRegionServerPage, FFLogsRegionServerPaginationIterator,
                    FFLogsServerCharacterPage, FFLogsServerCharacterPaginationIterator,
                    FFLogsSubregionServerPage, FFLogsSubregionServerPaginationIterator,)
from .region import FFLogsRegion, FFLogsSubregion
from .server import FFLogsServer
from .zone import FFLogsZone

__all__ = [
    # encounter.py
    'FFLogsEncounter',

    # expansion.py
    'FFLogsExpansion',

    # region.py
    'FFLogsRegion',
    'FFLogsSubregion',

    # server.py
    'FFLogsServer',

    # zone.py
    'FFLogsZone',

    # dataclasses.py
    'FFLogsPartition',

    # pages.py
    'FFLogsServerCharacterPage',
    'FFLogsServerCharacterPaginationIterator',
    'FFLogsRegionServerPage',
    'FFLogsRegionServerPaginationIterator',
    'FFLogsSubregionServerPage',
    'FFLogsSubregionServerPaginationIterator',
]
