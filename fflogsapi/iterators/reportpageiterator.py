from typing import TYPE_CHECKING, Dict

from fflogsapi.reports.report_page import FFLogsPage
import fflogsapi.queries as qs

if TYPE_CHECKING:
    from fflogsapi.client import FFLogsClient

class FFLogsReportPagesIterator:
    def __init__(self, client: 'FFLogsClient', filters: Dict[str, str] = {}) -> None:
        self._client = client
        self._cur_page = 0
        self._filters = filters

        filters = ', '.join([f'{key}: {f}' for key, f in filters.items()])
        result = self._client.q(qs.Q_REPORTPAGINATION.format(
            filters=filters,
            innerQuery='last_page',
        ))
        self._last_page = result['reportData']['reports']['last_page']
    
    def __iter__(self) -> 'FFLogsReportPagesIterator':
        return self

    def __next__(self) -> FFLogsPage:
        self._cur_page += 1
        if self._cur_page <= self._last_page:
            return FFLogsPage(
                page_num=self._cur_page,
                filters=self._filters,
                client=self._client,
            )
        else:
            self._cur_page = 0
            raise StopIteration
