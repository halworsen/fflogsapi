'''
Sadly, most of the world data is very tightly coupled, so the module structure is honestly horrible here.
Particularly, there are pagination classes in the region module.

There is, however, a sense of hierarchy to the classes contained in each module.
See their descriptions for more information.
'''
from .expansion import FFLogsExpansion, FFLogsZone, FFLogsEncounter
from .region import FFLogsRegion, FFLogsSubregion, FFLogsServer

__all__ = [
    'FFLogsEncounter',
    'FFLogsExpansion',
    'FFLogsRegion',
    'FFLogsSubregion',
    'FFLogsServer',
    'FFLogsZone',
]