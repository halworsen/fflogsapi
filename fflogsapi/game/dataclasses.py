from dataclasses import dataclass
from typing import Optional


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
