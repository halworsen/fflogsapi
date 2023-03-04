from dataclasses import dataclass
from typing import TYPE_CHECKING, Optional

from ..world.zone import FFLogsZone

if TYPE_CHECKING:
    from ..reports.report import FFLogsReport
    from .guild import FFLogsGuild


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
    zone: FFLogsZone


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
