from typing import TYPE_CHECKING, Any, Optional

from ..util.filters import construct_filter_string
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
    # The data fields of the objects in the page to retrieve
    DATA_FIELDS = []

    def __init__(self,
                 page_num: int,
                 filters: dict[str, str] = {},
                 client: 'FFLogsClient' = None,
                 additional_formatting: dict[str, str] = {},
                 ) -> None:
        self.page_num = page_num
        self.n_from = -1
        self.n_to = -1
        self.filters = filters.copy()
        self.additional_formatting = additional_formatting
        self.data = None
        self.objects = None

        self._client = client
        self._initialized = False

    def __iter__(self) -> 'FFLogsPageIterator':
        return FFLogsPageIterator(page=self)

    def __len__(self) -> int:
        return self.count()

    def _query_page(self) -> None:
        '''
        Retrieves metadata about data contained in this page.
        Specifically, IDs/codes are gathered and stored.
        '''
        self.filters['page'] = self.page_num
        filters = construct_filter_string(self.filters)
        data_fields = ','.join(self.DATA_FIELDS)
        page_data = self._client.q(self.PAGINATION_QUERY.format(
            filters=filters,
            innerQuery=Q_PAGE_META.format(dataFields=data_fields),
            **self.additional_formatting,
        ))
        page_data = itindex(page_data, self.PAGE_INDICES)

        self.n_from = page_data['from']
        self.n_to = page_data['to']
        self.data = page_data['data']
        self.objects = [None] * len(self.data)

        self._initialized = True

    def count(self) -> int:
        '''
        Returns:
            The amount of objects in this page.
        '''
        if not self._initialized:
            self._query_page()

        return (self.n_to - self.n_from) + 1

    def init_object(self, data: dict) -> Any:
        '''
        Initializes an instance of the object being paginated. Up to implementation.
        '''
        pass

    def object(self, idx: int) -> Optional[Any]:
        '''
        Get a specific object from this page.

        Args:
            idx: The page index of the object to retrieve from the page
        Returns:
            An object or None if the object is not contained in the page
        '''
        if not self._initialized:
            self._query_page()

        if idx < 0 or idx > len(self.data):
            return None

        if self.objects[idx] is None:
            self.objects[idx] = self.init_object(self.data[idx])

        return self.objects[idx]


class FFLogsPageIterator:
    '''
    Iterates over a page, returning the object being paginated
    '''

    def __init__(self, page: 'FFLogsPage') -> None:
        self._page = page
        self._cur_idx = -1
        self._max_amount = page.count()

    def __iter__(self) -> 'FFLogsPageIterator':
        return self

    def __next__(self) -> Any:
        self._cur_idx += 1
        if self._cur_idx < self._max_amount:
            return self._page.object(self._cur_idx)
        else:
            self._cur_idx = -1
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
        filters: dict[str, Any] = {},
        additional_formatting: dict[str, str] = {},
    ) -> None:
        '''
        If the pagination query requires any additional formatting,
        it can be specified using `additional_formatting`.
        '''
        self._client = client
        self._cur_page = 0
        self._filters = filters.copy()
        self.additional_formatting = additional_formatting

        pagination_filters = self._filters.copy()
        pagination_filters['page'] = 1
        filters = construct_filter_string(pagination_filters)
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
