from typing import TYPE_CHECKING, Any, Dict, List, Optional
from fflogsapi.util.filters import construct_filter_string
import fflogsapi.queries as qs

if TYPE_CHECKING:
    from fflogsapi.client import FFLogsClient

def fetch_data(key):
    '''
    Decorator that queries and stores the given key
    '''
    def decorator(func):
        def ensured(*args, **kwargs):
            self = args[0]
            if key not in self._data:
                result = self._query_data(key)
                self._data[key] = result['characterData']['character'][key]
            return func(*args, **kwargs)
        return ensured
    return decorator

class FFLogsCharacter:
    '''
    Representation of a character on FFLogs.
    '''

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
        filters = ', '.join([f'{key}: {f}' for key, f in self.filters.items()])
        result = self._client.q(qs.Q_CHARACTER_DATA.format(
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
        # A tiny bit of bookkeeping. Store the ID if we don't have it already, then use it to filter in the future
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

    @fetch_data('server')
    def server(self) -> str:
        '''
        Get the name of the server the character belongs to.

        Returns:
            The character's server.
        '''
        return self._data['server']

    @fetch_data('guildRank')
    def fc_rank(self) -> str:
        '''
        Get the FC rank of the character. This is game data, not FFLogs data.

        Returns:
            The character's FC rank.
        '''
        return self._data['guildRank']

    @fetch_data('gameData')
    def game_data(self) -> Dict:
        '''
        Get cached game data tied to the character, such as gear.

        Returns:
            The character's game data.
        '''
        return self._data['gameData']

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
        filter_string = construct_filter_string(filters)
        if filter_string != '':
            filter_string = f'({filter_string})'

        result = self._query_data(f'encounterRankings{filter_string}')
        return result['characterData']['character']['encounterRankings']

    def zone_rankings(self, filters: Dict[str, Any] = {}) -> Dict:
        '''
        Get this character's rankings for different zones (bosses).

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, zone ID, etc.
        Returns:
            The character's filtered ranking data.
        '''
        filter_string = construct_filter_string(filters)
        if filter_string != '':
            filter_string = f'({filter_string})'

        result = self._query_data(f'zoneRankings{filter_string}')
        return result['characterData']['character']['zoneRankings']
