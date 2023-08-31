'''
Various constant values that are typically useful for filtering queries.
'''

from enum import Enum


class FightDifficulty(Enum):
    UNKNOWN = None
    NORMAL = 100
    SAVAGE = 101


class PartySize(Enum):
    LIGHT = 4
    FULL = 8


class EventType(Enum):
    COMBATANT_INFO = 'combatantinfo'
    BEGINCAST = 'begincast'
    CAST = 'cast'
    DAMAGE = 'damage'
    CALCULATED_DAMAGE = 'calculateddamage'
    HEAL = 'heal'
    CALCULATED_HEAL = 'calculatedheal'
    ABSORBED = 'absorbed'
    APPLY_BUFF = 'applybuff'
    APPLY_BUFF_STACK = 'applybuffstack'
    REFRESH_BUFF = 'refreshbuff'
    REMOVE_BUFF = 'removebuff'
    REMOVE_BUFF_STACK = 'removebuffstack'
    APPLY_DEBUFF = 'applydebuff'
    REFRESH_DEBUFF = 'refreshdebuff'
    REMOVE_DEBUFF = 'removedebuff'
    LB_UPDATE = 'limitbreakupdate'
    ENCOUNTER_END = 'encounterend'


# FF Logs uses millisecond precision in its timestamps
TIMESTAMP_PRECISION = 1e-3
