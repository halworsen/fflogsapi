from ..data.page import FFLogsPage, FFLogsPaginationIterator
from .queries import Q_REPORT_PAGINATION
from .report import FFLogsReport


class FFLogsReportPage(FFLogsPage):
    '''
    Representation of a page of reports on FF Logs.
    '''

    PAGINATION_QUERY = Q_REPORT_PAGINATION
    PAGE_INDICES = ['reportData', 'reports']
    DATA_FIELDS = ['code']

    def init_object(self, data: dict) -> FFLogsReport:
        '''
        Initializes a report with the given code.
        '''
        return FFLogsReport(code=data['code'], client=self._client)


class FFLogsReportPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple report pages
    '''

    PAGE_CLASS = FFLogsReportPage
