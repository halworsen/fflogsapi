'''
Sadly, most of the world data is very tightly coupled,
so the module structure is honestly horrible here.
Particularly, there are pagination classes in the region module.

There is, however, a sense of hierarchy to the classes contained in each module.
See their descriptions for more information.
'''
from .expansion import FFLogsEncounter, FFLogsExpansion, FFLogsZone
from .region import FFLogsRegion, FFLogsServer, FFLogsSubregion

__all__ = [
    'FFLogsEncounter',
    'FFLogsExpansion',
    'FFLogsRegion',
    'FFLogsSubregion',
    'FFLogsServer',
    'FFLogsZone',
]
