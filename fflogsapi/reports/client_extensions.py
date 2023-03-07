from .pages import FFLogsReportPaginationIterator
from .report import FFLogsReport


class ReportsMixin:
    '''
    Client extensions to support report data exposed by the FF Logs API.
    '''

    def reports(self, filters: dict = {}) -> FFLogsReportPaginationIterator:
        '''
        Iterate over pages of FF Logs reports.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/reportdata.doc.html

        Args:
            filters: Filters to use when finding reports.
        Returns:
            An iterator over the pages of reports that match the given filters.
        '''
        return FFLogsReportPaginationIterator(filters=filters, client=self)

    def get_report(self, code: str) -> FFLogsReport:
        '''
        Retrieves the given report data from FF Logs.

        Args:
            code: The report code.
        Returns:
            A FFLogsReport object representing the report.
        '''
        return FFLogsReport(code=code, client=self)
