'''
fflogsapi
===

FF Logs API client. Start using the client by importing it:

```python
from fflogsapi import FFLogsClient
client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
```

The entire API should be accessible through the client. If you want typing, feel free to import
names from the relevant subpackages.
'''

from .client import FFLogsClient
from .constants import TIMESTAMP_PRECISION, EventType, FightDifficulty, PartySize
from .util.gql_enums import GQLEnum

__all__ = [
    # client.py
    'FFLogsClient',

    # constants.py
    'FightDifficulty',
    'PartySize',
    'EventType',
    'TIMESTAMP_PRECISION',

    # util/gql_enums.py
    'GQLEnum',
]
