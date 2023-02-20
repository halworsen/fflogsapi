from typing import TYPE_CHECKING

from fflogsapi.reports.fight import FFLogsFight

if TYPE_CHECKING:
    from fflogsapi.client import FFLogsClient
    from fflogsapi.reports.report import FFLogsReport

class FFLogsReportIterator:
    '''
    Iterates over a report, returning fights
    '''
    def __init__(self, report: 'FFLogsReport', client: 'FFLogsClient') -> None:
        self._report = report
        self._client = client
        self._cur_encounter = 0
        self._max_encounter = report.fight_count()
    
    def __iter__(self) -> 'FFLogsReportIterator':
        return self

    def __next__(self) -> 'FFLogsFight':
        self._cur_encounter += 1
        if self._cur_encounter <= self._max_encounter:
            return self._report.fight_by_id(self._cur_encounter)
        else:
            self._cur_encounter = 0
            raise StopIteration
