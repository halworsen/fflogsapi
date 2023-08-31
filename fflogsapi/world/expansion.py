from typing import TYPE_CHECKING, Any

from ..util.decorators import fetch_data
from ..util.indexing import itindex
from .queries import Q_EXPANSION

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from .zone import FFLogsZone


class FFLogsExpansion:
    '''
    Representation of an expansion on FF Logs.
    '''

    DATA_INDICES = ['worldData', 'expansion']

    id: int = -1
    ''' The ID of the expansion '''

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self.id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a expansion
        '''
        result = self._client.q(Q_EXPANSION.format(
            expansionID=self.id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the expansion's name.

        Returns:
            The expansion's name.
        '''
        return self._data['name']

    def zones(self) -> list['FFLogsZone']:
        '''
        Get a list of all zones within this expansion.

        Returns:
            A list of the expansion's zones.
        '''
        from .zone import FFLogsZone

        zones = self._query_data('zones{ id }')
        zone_ids = [e['id'] for e in zones['zones']]

        return [FFLogsZone(id=id, client=self._client) for id in zone_ids]
