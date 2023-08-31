from typing import TYPE_CHECKING, Any

from ..util.decorators import fetch_data
from ..util.filters import construct_filter_string
from ..util.indexing import itindex
from .queries import Q_ENCOUNTER

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from .zone import FFLogsZone


class FFLogsEncounter:
    '''
    Representation of an encounter on FF Logs.
    '''

    DATA_INDICES = ['worldData', 'encounter']

    id: int = -1
    ''' The ID of the encounter '''

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self.id = id
        self._data = {'id': id}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about an encounter
        '''
        result = self._client.q(Q_ENCOUNTER.format(
            encounterID=self.id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the encounter's name.

        Returns:
            The encounter's name.
        '''
        return self._data['name']

    def zone(self) -> 'FFLogsZone':
        '''
        Get the zone the encounter is found in.

        Returns:
            The encounter's zone.
        '''
        from .zone import FFLogsZone

        zone_id = self._query_data('zone{ id }')['zone']['id']
        return FFLogsZone(id=zone_id, client=self._client)

    def character_rankings(self, filters: dict[str, Any] = {}) -> dict:
        '''
        Get character/player ranking information for the encounter.
        Character ranking pagination for encounters must be handled by hand.

        For a full list of valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/encounter.doc.html

        Args:
            filters: Filters to use when retrieving character rankings for the encounter.
        Returns:
            The encounter's filtered character ranking data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'characterRankings{filters}')
        return result['characterRankings']

    def fight_rankings(self, filters: dict[str, Any] = {}) -> dict:
        '''
        Get fight rankings for the encounter.
        Fight ranking pagination for encounters must be handled by hand.

        For a full list of valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/encounter.doc.html

        Args:
            filters: Filters to use when retrieving fight rankings for the encounter.
        Returns:
            The encounter's filtered fight ranking data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'fightRankings{filters}')
        return result['fightRankings']
