from typing import TYPE_CHECKING, Any

from ..util.decorators import fetch_data
from ..util.indexing import itindex
from .queries import Q_REGION, Q_SUBREGION

if TYPE_CHECKING:
    from world.pages import (FFLogsRegionServerPaginationIterator,
                             FFLogsSubregionServerPaginationIterator,)

    from ..client import FFLogsClient


class FFLogsRegion:
    '''
    Representation of a region on FF Logs. These correspond to geographical server regions.
    '''

    DATA_INDICES = ['worldData', 'region']

    id: int = -1
    ''' The ID of the region '''

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self.id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a region
        '''
        result = self._client.q(Q_REGION.format(
            regionID=self.id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

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
        from .pages import FFLogsRegionServerPaginationIterator
        return FFLogsRegionServerPaginationIterator(
            client=self._client,
            additional_formatting={'regionID': self.id}
        )

    def subregions(self) -> list['FFLogsSubregion']:
        '''
        Get a list of subregions belonging to this region

        Returns:
            A list of subregions.
        '''
        subregions = self._query_data('subregions{ id }')['subregions']
        subregions = [d['id'] for d in subregions]
        if 'subregions' not in self._data:
            self._data['subregions'] = [FFLogsSubregion(
                id=id, client=self._client) for id in subregions]

        return self._data['subregions']


class FFLogsSubregion:
    '''
    Representation of a subregion on FF Logs. These correspond to data centers.
    '''

    DATA_INDICES = ['worldData', 'subregion']

    id: int = -1
    ''' The ID of the subregion '''

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self.id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a subregion
        '''
        result = self._client.q(Q_SUBREGION.format(
            subregionID=self.id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

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
        region = self._query_data('region{ id }')['region']['id']
        if 'region' not in self._data:
            self._data['region'] = FFLogsRegion(id=region, client=self._client)

        return self._data['region']

    def servers(self) -> 'FFLogsSubregionServerPaginationIterator':
        '''
        Get a list of all servers within this subregion/data center.

        Returns:
            A list of the subregion's servers.
        '''
        from .pages import FFLogsSubregionServerPaginationIterator
        return FFLogsSubregionServerPaginationIterator(
            client=self._client,
            additional_formatting={'subregionID': self.id}
        )
