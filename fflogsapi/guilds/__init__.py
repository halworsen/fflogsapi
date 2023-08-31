'''
Client extensions providing access to `guildData` in the v2 FF Logs API.
'''

from .dataclasses import (FFLogsAttendanceReport, FFLogsGuildZoneRankings, FFLogsRank,
                          FFLogsReportTag,)
from .guild import FFLogsGuild

__all__ = [
    # guild.py
    'FFLogsGuild',

    # dataclasses.py
    'FFLogsReportTag',
    'FFLogsAttendanceReport',
    'FFLogsRank',
    'FFLogsGuildZoneRankings',
]
