'''
Dataclasses and such.
'''

from .dataclasses import (FFAbility, FFGameZone, FFGrandCompany, FFItem, FFJob, FFLogsActor,
                          FFLogsAllStarsRanking, FFLogsArchivalData, FFLogsAttendanceReport,
                          FFLogsEncounterRankings, FFLogsFightRank, FFLogsGuildZoneRankings,
                          FFLogsNPCData, FFLogsPartition, FFLogsPlayerDetails, FFLogsRank,
                          FFLogsReportAbility, FFLogsReportCharacterRanking,
                          FFLogsReportComboRanking, FFLogsReportRanking, FFLogsReportTag,
                          FFLogsZoneEncounterRanking, FFLogsZoneRanking, FFMap,)

from .phases import PhaseType, PhaseInformation, OmegaPhaseData, AlexanderPhaseData, ALL_PHASE_DATA

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

    # .phases
    'PhaseType',
    'PhaseInformation',
    'OmegaPhaseData',
    'AlexanderPhaseData',
    'ALL_PHASE_DATA',
]
