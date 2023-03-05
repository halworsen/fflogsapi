from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from ..characters.character import FFLogsCharacter
    from ..game.dataclasses import FFJob
    from .report import FFLogsReport


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
