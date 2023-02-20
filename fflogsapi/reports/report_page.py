from typing import TYPE_CHECKING, Dict, Optional

from fflogsapi.iterators.pageiterator import FFLogsPageIterator
from fflogsapi.reports.report import FFLogsReport
import fflogsapi.queries as qs

if TYPE_CHECKING:
    from client import FFLogsClient

class FFLogsPage:
    '''
    Representation of a page of reports on FFLogs.
    '''

    def __init__(self,
        page_num: int,
        filters: Dict[str, str] = {},
        client: 'FFLogsClient' = None,
    ):
        self.page_num = page_num
        self.n_from = -1
        self.n_to = -1
        self.filters = filters
        self.reports = {}

        self._client = client
        self._initialized = False
        self._report_codes = []

        self._custom_filters = []
        for key, filter in filters.items():
            self._custom_filters.append(f'{key}: {filter}')

    def __iter__(self):
        return FFLogsPageIterator(page=self, client=self._client)

    def _query_page(self):
        '''
        Retrieves metadata about reports contained in this page.
        Specifically, report codes are gathered and stored.
        '''
        filters = ', '.join(self._custom_filters + [f'page: {self.page_num}'])
        page_data = self._client.q(qs.Q_REPORTPAGINATION.format(
            filters=filters,
            innerQuery=qs.Q_REPORT_PAGE_META,
        ))

        self.n_from = page_data['reportData']['reports']['from']
        self.n_to = page_data['reportData']['reports']['to']

        self._report_codes = []
        for report in page_data['reportData']['reports']['data']:
            self._report_codes.append(report['code'])
        
        self._initialized = True
    
    def report_count(self) -> int:
        '''
        Returns:
            The amount of reports in this page
        '''
        if not self._initialized:
            self._query_page()

        return (self.n_to - self.n_from) + 1

    def report(self, code) -> Optional[FFLogsReport]:
        '''
        Get a specific report from this page.

        Args:
            code: The code of the report to retrieve from the page
        Returns:
            A FFLogs report or None if the report is not contained in the page
        '''
        if not self._initialized:
            self._query_page()

        if code not in self._report_codes:
            return None

        if code not in self.reports:
            report = FFLogsReport(code=code, client=self._client)
            self.reports[code] = report

        return self.reports[code]
