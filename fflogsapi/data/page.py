from typing import TYPE_CHECKING, Any, Optional

from ..util.indexing import itindex
from .queries import Q_PAGE_META

if TYPE_CHECKING:
    from client import FFLogsClient


class FFLogsPage:
    '''
    Representation of a page of data on FFLogs.
    Base class for specific page types, do not use.
    '''

    # Base query from which to find pages
    PAGINATION_QUERY: str = ''
    # How to index the queried data to reach page metadata
    PAGE_INDICES: list = []
    # Field name of the ID/code of the object being paginated
    OBJECT_ID_FIELD: str = ''

    def __init__(self,
                 page_num: int,
                 filters: dict[str, str] = {},
                 client: 'FFLogsClient' = None,
                 additional_formatting: dict[str, str] = {},
                 ) -> None:
        self.page_num = page_num
        self.n_from = -1
        self.n_to = -1
        self.filters = filters
        self.additional_formatting = additional_formatting
        self.data = {}

        self._client = client
        self._initialized = False
        self._ids = []

        self._custom_filters = []
        for key, filter in filters.items():
            self._custom_filters.append(f'{key}: {filter}')

    def __iter__(self):
        return FFLogsPageIterator(page=self)

    def _query_page(self):
        '''
        Retrieves metadata about data contained in this page.
        Specifically, IDs/codes are gathered and stored.
        '''
        filters = ', '.join(self._custom_filters + [f'page: {self.page_num}'])
        page_data = self._client.q(self.PAGINATION_QUERY.format(
            filters=filters,
            innerQuery=Q_PAGE_META.format(idField=self.OBJECT_ID_FIELD),
            **self.additional_formatting,
        ))

        self.n_from = itindex(page_data, self.PAGE_INDICES)['from']
        self.n_to = itindex(page_data, self.PAGE_INDICES)['to']

        self._ids = []
        for object in itindex(page_data, self.PAGE_INDICES)['data']:
            self._ids.append(object[self.OBJECT_ID_FIELD])

        self._initialized = True

    def count(self) -> int:
        '''
        Returns:
            The amount of objects in this page.
        '''
        if not self._initialized:
            self._query_page()

        return (self.n_to - self.n_from) + 1

    def init_object(self, id: Any) -> Any:
        '''
        Initializes an instance of the object being paginated. Up to implementation.
        '''
        pass

    def object(self, id: Any) -> Optional[Any]:
        '''
        Get a specific object from this page.

        Args:
            id: The id of the object to retrieve from the page
        Returns:
            An object or None if the object is not contained in the page
        '''
        if not self._initialized:
            self._query_page()

        if id not in self._ids:
            return None

        if id not in self.data:
            object = self.init_object(id)
            self.data[id] = object

        return self.data[id]


class FFLogsPageIterator:
    '''
    Iterates over a page, returning the object being paginated
    '''

    def __init__(self, page: 'FFLogsPage') -> None:
        self._page = page
        self._cur_id = -1
        self._max_amount = page.count()

    def __iter__(self) -> 'FFLogsPageIterator':
        return self

    def __next__(self) -> Any:
        self._cur_id += 1
        if self._cur_id < self._max_amount:
            return self._page.object(self._page._ids[self._cur_id])
        else:
            self._cur_id = -1
            raise StopIteration


class FFLogsPaginationIterator:
    '''
    Iterates over multiple pages (a pagination), returning pages
    '''

    # The page class of the pages in the pagination
    PAGE_CLASS = None

    def __init__(
        self,
        client: 'FFLogsClient',
        filters: dict[str, str] = {},
        additional_formatting: dict[str, str] = {},
    ) -> None:
        '''
        If the pagination query requires any additional formatting,
        it can be specified using `additional_formatting`.
        '''
        self._client = client
        self._cur_page = 0
        self._filters = filters
        self.additional_formatting = additional_formatting

        filters = ', '.join([f'{key}: {f}' for key, f in filters.items()] + ['page: 1'])
        result = self._client.q(self.PAGE_CLASS.PAGINATION_QUERY.format(
            filters=filters,
            innerQuery='last_page',
            **additional_formatting,
        ))

        self._last_page = itindex(result, self.PAGE_CLASS.PAGE_INDICES)['last_page']

    def __iter__(self) -> 'FFLogsPaginationIterator':
        return self

    def __next__(self) -> FFLogsPage:
        self._cur_page += 1
        if self._cur_page <= self._last_page:
            return self.PAGE_CLASS(
                page_num=self._cur_page,
                filters=self._filters,
                client=self._client,
                additional_formatting=self.additional_formatting,
            )
        else:
            self._cur_page = 0
            raise StopIteration
