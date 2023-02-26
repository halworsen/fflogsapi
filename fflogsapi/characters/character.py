from typing import TYPE_CHECKING, Any, Dict

from ..util.decorators import fetch_data
from ..util.filters import construct_filter_string
from ..util.indexing import itindex
from .queries import Q_CHARACTER_DATA

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from ..world.server import FFLogsServer


class FFLogsCharacter:
    '''
    Representation of a character on FFLogs.
    '''

    DATA_INDICES = ['characterData', 'character']

    def __init__(self, filters: dict = {}, id: int = -1, client: 'FFLogsClient' = None) -> None:
        self.filters = filters.copy()
        if id != -1 and 'id' not in self.filters:
            self.filters['id'] = id

        self._id = self.filters['id'] if 'id' in self.filters else -1
        self._data = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> Dict[Any, Any]:
        '''
        Query for a specific piece of information about a character
        '''
        filters = construct_filter_string(self.filters)
        result = self._client.q(Q_CHARACTER_DATA.format(
            filters=filters,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    @fetch_data('id')
    def id(self) -> int:
        '''
        Get the character's ID.

        Returns:
            The character's ID.
        '''
        # A tiny bit of bookkeeping. Store the ID if we don't have it already,
        # then use it to filter in the future
        if self._id == -1:
            self._id = self._data['id']
            self.filters = {'id': self._id}
        return self._data['id']

    @fetch_data('lodestoneID')
    def lodestone_id(self) -> int:
        '''
        Get the character's Lodestone ID.

        Returns:
            The character's Lodestone ID.
        '''
        return self._data['lodestoneID']

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the character's name.

        Returns:
            The character's name.
        '''
        return self._data['name']

    def server(self) -> 'FFLogsServer':
        '''
        Get the server the character belongs to.

        Returns:
            The character's server.
        '''
        from ..world.server import FFLogsServer
        server_id = itindex(self._query_data('server{ id }'), self.DATA_INDICES)['server']['id']
        return FFLogsServer(filters={'id': server_id}, client=self._client)

    @fetch_data('guildRank')
    def fc_rank(self) -> str:
        '''
        Get the FC rank of the character. This is game data, not FFLogs data.

        Returns:
            The character's FC rank.
        '''
        return self._data['guildRank']

    def game_data(self, filters: dict = {}) -> dict:
        '''
        Get cached game data tied to the character, such as gear.

        Args:
            filters: Filter game data to a specific specID or force an update by the API.
        Returns:
            The character's game data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'gameData{filters}')
        return itindex(result, self.DATA_INDICES)['gameData']

    @fetch_data('hidden')
    def hidden(self) -> bool:
        '''
        Whether or not the character's rankings are hidden.

        Returns:
            True if the rankings are hidden, False otherwise.
        '''
        return self._data['hidden']

    def encounter_rankings(self, filters: Dict[str, Any] = {}) -> Dict:
        '''
        Get this character's rankings for different encounters. Encounter ID is mandatory.

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, encounter ID, etc.
        Returns:
            The character's filtered ranking data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'encounterRankings{filters}')
        return itindex(result, self.DATA_INDICES)['encounterRankings']

    def zone_rankings(self, filters: Dict[str, Any] = {}) -> Dict:
        '''
        Get this character's rankings for different zones (bosses).

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, zone ID, etc.
        Returns:
            The character's filtered ranking data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'zoneRankings{filters}')
        return itindex(result, self.DATA_INDICES)['zoneRankings']
