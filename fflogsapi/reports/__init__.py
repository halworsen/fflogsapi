'''
Client extensions providing access to `reportData` in the v2 FF Logs API.
'''

from .dataclasses import (FFGameZone, FFLogsActor, FFLogsArchivalData, FFLogsNPCData,
                          FFLogsPlayerDetails, FFLogsReportAbility, FFLogsReportCharacterRanking,
                          FFLogsReportComboRanking, FFLogsReportRanking,)
from .fight import FFLogsFight
from .pages import FFLogsReportPage, FFLogsReportPaginationIterator
from .report import FFLogsReport

__all__ = [
    # report.py
    'FFLogsReport',

    # fight.py
    'FFLogsFight',

    # dataclasses.py
    'FFLogsActor',
    'FFLogsReportAbility',
    'FFLogsArchivalData',
    'FFLogsPlayerDetails',
    'FFLogsReportCharacterRanking',
    'FFLogsReportComboRanking',
    'FFLogsReportRanking',
    'FFLogsNPCData',
    'FFGameZone',

    # pages.py
    'FFLogsReportPage',
    'FFLogsReportPaginationIterator',
]
