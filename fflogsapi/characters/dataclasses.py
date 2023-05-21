from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..game.dataclasses import FFJob
    from ..guilds.guild import FFLogsGuild
    from ..reports.fight import FFLogsFight
    from ..world.encounter import FFLogsEncounter
    from ..world.zone import FFLogsZone


@dataclass
class FFLogsAllStarsRanking:
    '''
    All stars ranking information
    '''
    partition: int
    job: 'FFJob'
    points: float
    possible_points: int
    rank: int
    region_rank: int
    server_rank: int
    rank_percent: float
    total: int


@dataclass
class FFLogsFightRank:
    '''
    Rank information from one fight
    '''
    locked_in: bool
    bracket_data: str

    rank_percent: float
    rank_total_parses: int

    today_percent: float
    today_total_parses: int

    historical_percent: float
    historical_total_parses: int

    guild: Optional['FFLogsGuild']
    fight: 'FFLogsFight'

    job: 'FFJob'
    best_job: 'FFJob'

    adps: float
    rdps: float
    ndps: float
    pdps: float


@dataclass
class FFLogsEncounterRankings:
    '''
    Ranking information for a character on a specific encounter (boss)
    '''
    zone: 'FFLogsZone'
    metric: str
    best_amount: float
    average_performance: float
    median_performance: float
    kills: int
    fastest_kill: int
    difficulty: int
    ranks: list['FFLogsFightRank']


@dataclass
class FFLogsZoneEncounterRanking:
    '''
    Zone ranking information for a character for a specific encounter
    '''
    locked_in: bool

    encounter: 'FFLogsEncounter'

    rank_percent: float
    median_percent: float
    best_amount: float

    kills: int
    fastest_kill: int

    all_stars: FFLogsAllStarsRanking

    job: 'FFJob'
    best_job: 'FFJob'


@dataclass
class FFLogsZoneRanking:
    '''
    Ranking information for a character in a specific zone

    Note that `all_stars` is a list of all stars rankings for different partitions
    '''
    zone: 'FFLogsZone'
    metric: str
    encounter_ranks: list[FFLogsZoneEncounterRanking]
    difficulty: int
    best_performance_avg: float
    median_performance_avg: float
    all_stars: list[FFLogsAllStarsRanking]
