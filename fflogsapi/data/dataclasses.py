from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from fflogsapi.util.decorators import default_instantiation

if TYPE_CHECKING:
    from ..characters.character import FFLogsCharacter
    from ..guilds.guild import FFLogsGuild
    from ..reports.fight import FFLogsFight
    from ..reports.report import FFLogsReport
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

    adps: Optional[float]
    rdps: Optional[float]
    ndps: Optional[float]
    pdps: Optional[float]


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


@dataclass
class FFLogsReportCharacterRanking:
    '''
    Ranking information for a single character as provided by a report.

    `amount` is ambiguous and depends on the metric asked for.
    You'll just have to keep track yourself.

    `rank` and `best_rank` are strings because the ranking may be approximate. If the rank begins
    with a '~', that means the rank is approximate.
    '''
    character: 'FFLogsCharacter'
    job: 'FFJob'
    amount: float
    rank: str
    best_rank: str
    total_parses: int
    percentile: int


@dataclass
class FFLogsReportComboRanking:
    '''
    Ranking information for a combination of two tanks/healers.

    `type` is either 'tanks' or 'healers' to indicate what kind of combination ranking this is.
    '''
    type: str
    character_a: 'FFLogsCharacter'
    character_b: 'FFLogsCharacter'
    job_a: 'FFJob'
    job_b: 'FFJob'
    amount: float
    rank: str
    best_rank: str
    total_parses: int
    percentile: int


@dataclass
class FFLogsReportRanking:
    '''
    Ranking information provided by a report.

    Combo rankings are tank/healer combination rankings, i.e. the rank of both tanks/healers
    combined.
    '''
    patch: float
    bracket: int
    deaths: int
    damage_taken_not_tanks: int
    character_rankings: list[FFLogsReportCharacterRanking]
    combo_rankings: list[FFLogsReportComboRanking]


@dataclass
class FFAbility:
    '''
    A FFXIV ability.

    The type field is only set if the ability is retrieved from a report as they are the only
    data objects through which the API will return that information.
    '''
    id: int
    name: str
    description: str
    icon: str
    type: Optional[int] = None


@dataclass
class FFItem:
    '''
    A FFXIV item.
    '''
    id: int
    name: str
    icon: str


@dataclass
class FFJob:
    '''
    A FFXIV job, called spec by the FF Logs API.
    '''
    id: int
    name: str
    slug: str

    def __eq__(self, other):
        return (self.id == other.id or self.slug == other.slug)


@default_instantiation
class FFJobInvalid(FFJob):
    '''
    A job that isn't supported by FFLogs.
    '''
    __default_args__ = [-1, 'Invalid Job', 'Invalid']


@dataclass
class FFGrandCompany:
    '''
    A grand company.
    '''
    id: int
    name: str


@dataclass
class FFMap:
    '''
    A FFXIV map.

    The filename refers to the file name of the image for the map. If None, there is no such image
    available.
    '''
    id: int
    name: str
    filename: str
    offset_x: int
    offset_y: int
    size_factor: int


@dataclass
class FFLogsReportTag:
    '''
    A tag used by a specific guild to categorize the guild's reports.
    '''
    id: int
    name: str
    guild: 'FFLogsGuild'


@dataclass
class FFLogsAttendanceReport:
    '''
    An attendance report belonging to a guild. The attendance report consists of a report and
    an accompanying list of attendance statuses for players.

    The players list contains tuples of the form (name, presence, job) where the presence value
    indicates what capacity the player presented in. A presence value of 1 indicates the player
    was present, while a presence value of 2 indicates the player was present on bench.
    '''
    report: 'FFLogsReport'
    players: tuple[tuple[str, int, str]]
    start: float
    zone: 'FFLogsZone'


@dataclass
class FFLogsRank:
    '''
    Ranking information for the world, relevant region and server.

    The number is the ordinal rank for the ranking metric, i.e. "Rank #N".
    The percentile is the 0-100 percentile score of the rank. This is unused by guild rankings.
    The color string is the color class used internally by FF Logs.
    '''
    number: int
    percentile: Optional[int]
    color: str


@dataclass
class FFLogsGuildZoneRankings:
    '''
    Ranking information for a specific guild, for a specific zone.

    For each ranking metric, there is a subdivision into world, region and server rank.

    completion_speed refers to the complete raid speed ranks for the guild.
    progress ranks the guild's progression through the zone.
    speed is the all-star based speed ranking for the guild in the zone.
    '''
    completion_speed: Optional[tuple[FFLogsRank]]
    progress: Optional[tuple[FFLogsRank]]
    speed: Optional[tuple[FFLogsRank]]


@dataclass
class FFLogsActor:
    '''
    Represents an actor in a report.
    '''
    report: 'FFLogsReport'
    id: int
    name: str
    type: str
    sub_type: str
    server: str
    game_id: int
    job: Optional['FFJob']
    pet_owner: 'FFLogsActor'


@dataclass
class FFLogsReportAbility:
    '''
    A game ability as represented in a report.

    These are slightly different than game abilities as they contain an additional
    type field indicating damage type.

    You can get more information about the ability for querying for the ability with `game_id`.
    '''
    game_id: int
    name: str
    type: int


@dataclass
class FFLogsArchivalData:
    '''
    Archivation data for a report.

    `accessible` denotes if the current user can access the report. `date` is the archival date, if
    the report is archived.
    '''
    archived: bool
    accessible: bool
    date: Optional[int]


@dataclass
class FFLogsPlayerDetails:
    '''
    Player details as provided by FF Logs for individual fights in a report.

    Note that most of the data here is only partially complete. For example, server name is
    given but server region is not. Spec information empty/useless as FFXIV does not have them,
    and there is no gear information.
    '''
    id: int
    actor: FFLogsActor
    guid: int
    name: str
    server: str
    job: 'FFJob'
    role: str


@dataclass
class FFLogsNPCData:
    '''
    NPC data as provided by a fight in a report.

    `group_count` is how many packs of the NPC were seen during the fight.

    `id` is the report ID of the NPC, and can be used to filter by source and target in the report.

    `instanceCount` is how many instances of the NPC were seen in the fight.

    If this NPC is a pet, `pet_owner` is the report ID of the pet owner.
    '''
    id: int
    actor: FFLogsActor
    hostile: bool
    game_id: int
    group_count: int
    instance_count: int
    pet_owner: FFLogsActor


@dataclass
class FFGameZone:
    '''
    A named in-game zone.
    '''
    id: int
    name: str


@dataclass
class FFLogsPartition:
    '''
    A partition within a zone.
    '''
    id: int
    name: str
    compact_name: str
    default: bool


@dataclass
class FFLogsPhase:
    '''
    Phase information for an encounter

    The encounter is not part of this dataclass because it can
    be queried from the fight from which this information was gotten
    '''
    id: int
    name: str
    intermission: bool
    separates_wipes: bool
    ''' Does this visually distinguish wipes in the FF Logs report UI? '''
