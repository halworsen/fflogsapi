from dataclasses import dataclass
from typing import Optional

from ..game.dataclasses import FFJob


@dataclass
class FFLogsActor:
    '''
    Represents an actor in a report
    '''
    id: int
    name: str
    type: str
    sub_type: str
    server: str
    game_id: int
    job: Optional[FFJob]
    pet_owner: Optional[int]


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
