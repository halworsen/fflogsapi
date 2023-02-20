from typing import TYPE_CHECKING, Dict, Optional

from fflogsapi.data.page import FFLogsPage, FFLogsPaginationIterator
from fflogsapi.reports.report import FFLogsReport
import fflogsapi.queries as qs

class FFLogsReportPage(FFLogsPage):
    '''
    Representation of a page of reports on FFLogs.
    '''

    # Base query from which to find pages
    PAGINATION_QUERY: str = qs.Q_REPORT_PAGINATION
    # Inner query to retrieve page metadata from
    PAGE_META_QUERY: str = qs.Q_REPORT_PAGE_META
    # What kind of object the page contains
    PAGE_TYPE: str = 'report'
    # Field name of the ID/code of the object being paginated
    OBJECT_ID_FIELD: str = 'code'

    def init_object(self, code: str) -> FFLogsReport:
        '''
        Initializes a report with the given ID (code).
        '''
        return FFLogsReport(code=code, client=self._client)

class FFLogsReportPaginationIterator(FFLogsPaginationIterator):
    '''
    Iterates over multiple pages (a pagination), returning pages
    '''

    # Base query from which to find pages
    PAGINATION_QUERY = qs.Q_REPORT_PAGINATION
    # What kind of object the pages contain
    PAGE_TYPE: str = 'report'
