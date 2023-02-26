from typing import TYPE_CHECKING, Any

from ..util.decorators import fetch_data
from ..util.indexing import itindex
from .pages import FFLogsServerCharacterPaginationIterator
from .queries import Q_SERVER

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from .region import FFLogsRegion, FFLogsSubregion


class FFLogsServer:
    '''
    Representation of a server on FFLogs.
    '''

    DATA_INDICES = ['worldData', 'server']

    def __init__(self, filters: dict = {}, client: 'FFLogsClient' = None) -> None:
        self.filters = filters.copy()
        self._data = {}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a server
        '''
        filters = ', '.join([f'{key}: {f}' for key, f in self.filters.items()])
        result = self._client.q(Q_SERVER.format(
            filters=filters,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    @fetch_data('id')
    def id(self) -> int:
        '''
        Get the server's ID.

        Returns:
            The server's ID.
        '''
        return self._data['id']

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the server's name. E.g. Lich, Tonberry, Siren, etc.

        Returns:
            The server's name.
        '''
        return self._data['name']

    @fetch_data('normalizedName')
    def normalized_name(self) -> str:
        '''
        Get the server's normalized name. This is the server name without spaces.

        Returns:
            The server's normalized name.
        '''
        return self._data['normalizedName']

    @fetch_data('slug')
    def slug(self) -> str:
        '''
        Get the server's slug. This is usually the exact same as the server's compact name

        Returns:
            The server's slug.
        '''
        return self._data['slug']

    def region(self) -> 'FFLogsRegion':
        '''
        Get the server's region. This is the geographical region in which the server resides.

        Returns:
            The server's region.
        '''
        from .region import FFLogsRegion

        region = itindex(self._query_data('region{ id }'), self.DATA_INDICES)['region']['id']
        if 'region' not in self._data:
            self._data['region'] = FFLogsRegion(id=region, client=self._client)

        return self._data['region']

    def subregion(self) -> 'FFLogsSubregion':
        '''
        Get the server's subregion, AKA data center.

        Returns:
            The server's subregion.
        '''
        from .region import FFLogsSubregion

        subregion = itindex(self._query_data('subregion{ id }'), self.DATA_INDICES)[
            'subregion']['id']
        if 'subregion' not in self._data:
            self._data['subregion'] = FFLogsSubregion(id=subregion, client=self._client)

        return self._data['subregion']

    def characters(self) -> FFLogsServerCharacterPaginationIterator:
        '''
        Get a pagination of all characters found on the server.

        Returns:
            A pagination iterator over all pages of characters belonging to the server.
        '''
        return FFLogsServerCharacterPaginationIterator(
            client=self._client,
            additional_formatting={'serverID': self.id()}
        )
