from dataclasses import dataclass


@dataclass
class FFLogsPartition:
    '''
    A partition within a zone.
    '''
    id: int
    name: str
    compact_name: str
    default: bool
