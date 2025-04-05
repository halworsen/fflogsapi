'''
Dataclasses and such.
'''

from fflogsapi.data.dataclasses import (FFAbility, FFGameZone, FFGrandCompany, FFItem, FFJob,
                                        FFJobInvalid, FFLogsActor, FFLogsAllStarsRanking,
                                        FFLogsArchivalData, FFLogsAttendanceReport,
                                        FFLogsEncounterRankings, FFLogsFightRank,
                                        FFLogsGuildZoneRankings, FFLogsNPCData, FFLogsPartition,
                                        FFLogsPhase, FFLogsPlayerDetails, FFLogsRank,
                                        FFLogsReportAbility, FFLogsReportCharacterRanking,
                                        FFLogsReportComboRanking, FFLogsReportRanking,
                                        FFLogsReportTag, FFLogsZoneEncounterRanking,
                                        FFLogsZoneRanking, FFMap,)

__all__ = [
    # dataclasses.py
    'FFLogsAllStarsRanking',
    'FFLogsFightRank',
    'FFLogsEncounterRankings',
    'FFLogsZoneEncounterRanking',
    'FFLogsZoneRanking',
    'FFLogsReportCharacterRanking',
    'FFLogsReportComboRanking',
    'FFLogsReportRanking',
    'FFAbility',
    'FFItem',
    'FFJob',
    'FFJobInvalid',
    'FFGrandCompany',
    'FFMap',
    'FFLogsReportTag',
    'FFLogsAttendanceReport',
    'FFLogsRank',
    'FFLogsGuildZoneRankings',
    'FFLogsActor',
    'FFLogsReportAbility',
    'FFLogsArchivalData',
    'FFLogsPlayerDetails',
    'FFLogsNPCData',
    'FFGameZone',
    'FFLogsPartition',
    'FFLogsPhase',
]
