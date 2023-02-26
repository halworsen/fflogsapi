from typing import TYPE_CHECKING, Any

from ..util.decorators import fetch_data
from .queries import Q_EXPANSION

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from .zone import FFLogsZone


class FFLogsExpansion:
    '''
    Representation of an expansion on FFLogs.
    '''

    DATA_INDICES = ['worldData', 'expansion']

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self._id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a expansion
        '''
        result = self._client.q(Q_EXPANSION.format(
            expansionID=self._id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def id(self) -> int:
        '''
        Get the expansion's ID.

        Returns:
            The expansion's ID.
        '''
        return self._id

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
        zone_ids = [e['id'] for e in zones['worldData']['expansion']['zones']]

        return [FFLogsZone(id=id, client=self._client) for id in zone_ids]
