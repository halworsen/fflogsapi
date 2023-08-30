'''
FF Logs API client. Start using the client by importing it:

    ```python
    from fflogsapi import FFLogsClient
    # alternatively
    from fflogsapi.client import FFLogsClient

    client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
    ```
'''

from .client import FFLogsClient
from .constants import FightDifficulty, PartySize, EventType
# deprecated in 2.0.0
from .constants import (EVENT_ENCOUNTER_END, EVENT_TYPE_APPLY_BUFF, EVENT_TYPE_APPLY_DEBUFF,
                        EVENT_TYPE_BEGINCAST, EVENT_TYPE_CALCULATED_DAMAGE, EVENT_TYPE_CAST,
                        EVENT_TYPE_COMBATANT_INFO, EVENT_TYPE_DAMAGE, EVENT_TYPE_HEAL,
                        EVENT_TYPE_LB_UPDATE, EVENT_TYPE_REFRESH_BUFF, EVENT_TYPE_REMOVE_BUFF,
                        FIGHT_DIFFICULTY_RAID, FIGHT_DIFFICULTY_SAVAGE, FIGHT_DIFFICULTY_UNKNOWN,)
# deprecation end

__all__ = [
    FFLogsClient,

    FightDifficulty,
    PartySize,
    EventType,

    # deprecated in 2.0.0
    FIGHT_DIFFICULTY_UNKNOWN,
    FIGHT_DIFFICULTY_RAID,
    FIGHT_DIFFICULTY_SAVAGE,
    EVENT_TYPE_COMBATANT_INFO,
    EVENT_TYPE_BEGINCAST,
    EVENT_TYPE_CAST,
    EVENT_TYPE_DAMAGE,
    EVENT_TYPE_HEAL,
    EVENT_TYPE_CALCULATED_DAMAGE,
    EVENT_TYPE_APPLY_BUFF,
    EVENT_TYPE_REFRESH_BUFF,
    EVENT_TYPE_REMOVE_BUFF,
    EVENT_TYPE_LB_UPDATE,
    EVENT_TYPE_APPLY_DEBUFF,
    EVENT_ENCOUNTER_END,
    # deprecation end
]
