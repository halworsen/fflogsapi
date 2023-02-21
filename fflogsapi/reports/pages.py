from fflogsapi.data.page import FFLogsPage, FFLogsPaginationIterator
from fflogsapi.reports.report import FFLogsReport
import fflogsapi.reports.queries as qs

class FFLogsReportPage(FFLogsPage):
    '''
    Representation of a page of reports on FFLogs.
    '''

    PAGINATION_QUERY = qs.Q_REPORT_PAGINATION
    PAGE_INDICES = ['reportData', 'reports']
    OBJECT_ID_FIELD = 'code'

    def init_object(self, code: str) -> FFLogsReport:
        '''
        Initializes a report with the given ID (code).
        '''
        return FFLogsReport(code=code, client=self._client)

class FFLogsReportPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple report pages
    '''

    PAGE_CLASS = FFLogsReportPage
