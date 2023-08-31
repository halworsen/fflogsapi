
from typing import TYPE_CHECKING, Any

from ..characters.character import FFLogsCharacter
from ..util.decorators import fetch_data
from ..util.indexing import itindex
from .queries import Q_USER

if TYPE_CHECKING:
    from client import FFLogsClient

    from ..guilds.guild import FFLogsGuild


class FFLogsUser:
    '''
    FF Logs user information object.
    '''

    DATA_INDICES = ['userData', 'user']

    id: int = -1
    ''' The ID of the user '''

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self.id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a user
        '''
        result = self._client.q(Q_USER.format(
            userID=self.id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the name of the user.

        Returns:
            The name of the user.
        '''
        return self._data['name']

    def characters(self) -> list[FFLogsCharacter]:
        '''
        Query for a list of all characters claimed by the user.

        This is only available when the client is in user mode. If the client is in client mode,
        the API will return an error stating that you do not have permission to view the user's
        claimed characters.

        Returns:
            A list of characters claimed by the user.
        '''
        characters = self._query_data('characters { id }')['characters']
        ids = [c['id'] for c in characters]

        return [FFLogsCharacter(id=id, client=self._client) for id in ids]

    def guilds(self) -> list['FFLogsGuild']:
        '''
        Get a list of all the guilds the user belongs to.

        This is only available when the client is in user mode. If the client is in client mode,
        the API will return an error stating that you do not have permission to view the user's
        claimed characters.

        Returns:
            A list of guilds the user belongs to.
        '''
        from ..guilds.guild import FFLogsGuild
        guilds = self._query_data('guilds { id }')['guilds']
        ids = [guild['id'] for guild in guilds]

        return [FFLogsGuild(id=id, client=self._client) for id in ids]
