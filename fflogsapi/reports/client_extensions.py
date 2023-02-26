from .pages import FFLogsReportPaginationIterator
from .report import FFLogsReport


class ReportsMixin:
    def report_pages(self, filters: dict = {}) -> FFLogsReportPaginationIterator:
        '''
        Iterate over pages of FFLogs reports.

        Args:
            filters: A dictionary containing filters to use when retrieving reports.
        Returns:
            An iterator over the pages of reports that match the given filters.
        '''
        return FFLogsReportPaginationIterator(filters=filters, client=self)

    def get_report(self, code: str) -> FFLogsReport:
        '''
        Retrieves the given report data from FFLogs.

        Args:
            code: The report code.
        Returns:
            A FFLogsReport object representing the report.
        '''
        return FFLogsReport(code=code, client=self)
