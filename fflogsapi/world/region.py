'''
The region module contains the class definitions for regions, subregions and servers.
FFLogs' hierarchy for servers is region (geographical region) -> subregion (datacenter) -> server
'''

from typing import TYPE_CHECKING, Any

from fflogsapi.data.page import FFLogsPage, FFLogsPaginationIterator

from ..util.decorators import fetch_data
from ..util.indexing import itindex
from .pages import FFLogsServerCharacterPaginationIterator
from .queries import (Q_REGION, Q_REGION_SERVER_PAGINATION, Q_SERVER, Q_SUBREGION,
                      Q_SUBREGION_SERVER_PAGINATION,)

if TYPE_CHECKING:
    from ..client import FFLogsClient


class FFLogsRegion:
    '''
    Representation of a region on FFLogs. These correspond to geographical server regions.
    '''

    DATA_INDICES = ['worldData', 'region']

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self._id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a region
        '''
        result = self._client.q(Q_REGION.format(
            regionID=self._id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def id(self) -> int:
        '''
        Get the region's ID.

        Returns:
            The region's ID.
        '''
        return self._id

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the region's name. E.g. Europe, North America, etc.

        Returns:
            The region's name.
        '''
        return self._data['name']

    @fetch_data('compactName')
    def compact_name(self) -> str:
        '''
        Get the region's compact name. E.g. 'EU' for Europe, 'NA' for North America, etc.

        Returns:
            The region's compact name.
        '''
        return self._data['compactName']

    @fetch_data('slug')
    def slug(self) -> str:
        '''
        Get the region's slug. This is usually the exact same as the region's compact name

        Returns:
            The region's slug.
        '''
        return self._data['slug']

    def servers(self) -> 'FFLogsRegionServerPaginationIterator':
        '''
        Get a pagination of all servers in the region.

        Returns:
            A pagination iterator of the region's servers.
        '''
        return FFLogsRegionServerPaginationIterator(
            client=self._client,
            additional_formatting={'regionID': self._id}
        )

    def subregions(self) -> list['FFLogsSubregion']:
        '''
        Get a list of subregions belonging to this region

        Returns:
            A list of subregions.
        '''
        subregions = itindex(self._query_data('subregions{ id }'), self.DATA_INDICES)['subregions']
        subregions = [d['id'] for d in subregions]
        if 'subregions' not in self._data:
            self._data['subregions'] = [FFLogsSubregion(
                id=id, client=self._client) for id in subregions]

        return self._data['subregions']


class FFLogsSubregion:
    '''
    Representation of a subregion on FFLogs. These correspond to data centers.
    '''

    DATA_INDICES = ['worldData', 'subregion']

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self._id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a subregion
        '''
        result = self._client.q(Q_SUBREGION.format(
            subregionID=self._id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def id(self) -> int:
        '''
        Get the subregion's ID.

        Returns:
            The subregion's ID.
        '''
        return self._id

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the subregion's name. E.g. Light, Crystal, Mana, etc.

        Returns:
            The subregion's name.
        '''
        return self._data['name']

    def region(self) -> FFLogsRegion:
        '''
        Get the subregion's parent region.
        This is the geographical region in which the data center resides.

        Returns:
            The subregion's parent region.
        '''
        region = itindex(self._query_data('region{ id }'), self.DATA_INDICES)['region']['id']
        if 'region' not in self._data:
            self._data['region'] = FFLogsRegion(id=region, client=self._client)

        return self._data['region']

    def servers(self) -> 'FFLogsSubregionServerPaginationIterator':
        '''
        Get a list of all servers within this subregion/data center.

        Returns:
            A list of the subregion's servers.
        '''
        return FFLogsSubregionServerPaginationIterator(
            client=self._client,
            additional_formatting={'subregionID': self._id}
        )


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
        Get the server's name. E.g. Europe, North America, etc.

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

    def region(self) -> FFLogsRegion:
        '''
        Get the server's region. This is the geographical region in which the data center resides.

        Returns:
            The server's region.
        '''
        region = itindex(self._query_data('region{ id }'), self.DATA_INDICES)['region']['id']
        if 'region' not in self._data:
            self._data['region'] = FFLogsRegion(id=region, client=self._client)

        return self._data['region']

    def subregion(self) -> FFLogsSubregion:
        '''
        Get the server's subregion, AKA data center.

        Returns:
            The server's subregion.
        '''
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


class FFLogsRegionServerPage(FFLogsPage):
    '''
    Represents a page of a region's servers on FFLogs.
    '''

    PAGINATION_QUERY = Q_REGION_SERVER_PAGINATION
    PAGE_INDICES = ['worldData', 'region', 'servers']
    OBJECT_ID_FIELD = 'id'

    def init_object(self, id: int) -> FFLogsServer:
        '''
        Initializes a server with the given ID.
        '''
        return FFLogsServer(filters={'id': id}, client=self._client)


class FFLogsRegionServerPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages of a region's servers
    '''

    PAGE_CLASS = FFLogsRegionServerPage


class FFLogsSubregionServerPage(FFLogsRegionServerPage):
    '''
    Represents a page of a subregion's servers on FFLogs.
    '''

    PAGINATION_QUERY = Q_SUBREGION_SERVER_PAGINATION
    PAGE_INDICES = ['worldData', 'subregion', 'servers']


class FFLogsSubregionServerPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages of a subregion's servers
    '''

    PAGE_CLASS = FFLogsSubregionServerPage
