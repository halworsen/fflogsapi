from typing import TYPE_CHECKING

from ..characters.pages import FFLogsCharacterPage
from ..data.page import FFLogsPage, FFLogsPaginationIterator
from .queries import (Q_REGION_SERVER_PAGINATION, Q_SERVER_CHARACTER_PAGINATION,
                      Q_SUBREGION_SERVER_PAGINATION,)

if TYPE_CHECKING:
    from .server import FFLogsServer


class FFLogsServerCharacterPage(FFLogsCharacterPage):
    '''
    Represents a page of a server's characters on FFLogs.
    '''

    PAGINATION_QUERY = Q_SERVER_CHARACTER_PAGINATION
    PAGE_INDICES = ['worldData', 'server', 'characters']


class FFLogsServerCharacterPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages of a server's characters.
    '''

    PAGE_CLASS = FFLogsServerCharacterPage


class FFLogsRegionServerPage(FFLogsPage):
    '''
    Represents a page of a region's servers on FFLogs.
    '''

    PAGINATION_QUERY = Q_REGION_SERVER_PAGINATION
    PAGE_INDICES = ['worldData', 'region', 'servers']
    OBJECT_ID_FIELD = 'id'

    def init_object(self, id: int) -> 'FFLogsServer':
        '''
        Initializes a server with the given ID.
        '''
        from .server import FFLogsServer
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
