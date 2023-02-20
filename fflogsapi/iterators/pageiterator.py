from typing import TYPE_CHECKING
from fflogsapi.reports.report import FFLogsReport

if TYPE_CHECKING:
    from fflogsapi.client import FFLogsClient
    from fflogsapi.reports.report_page import FFLogsPage

class FFLogsPageIterator:
    def __init__(self, page: 'FFLogsPage', client: 'FFLogsClient') -> None:
        self._page = page
        self._client = client
        self._cur_report = -1
        self._max_amount = page.report_count()
    
    def __iter__(self) -> 'FFLogsPageIterator':
        return self
    
    def __next__(self) -> FFLogsReport:
        self._cur_report += 1
        if self._cur_report < self._max_amount:
            return FFLogsReport(
                self._page._report_codes[self._cur_report],
                client=self._client,
            )

        else:
            self._cur_report = 0
            raise StopIteration
