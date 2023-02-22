import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.reports.fight import FFLogsFight
from fflogsapi.reports.pages import FFLogsReportPage
from fflogsapi.reports.report import FFLogsReport
from .config import *

class ReportTest(unittest.TestCase):
    '''
    Test cases for FFLogs reports.

    This test case makes assumptions on the availability of a specific report.
    If the tests break, it may be because visibility settings were changed or the report was deleted.
    '''

    SPECIFIC_REPORT_CODE = '2Kf9y6wzanWkBJ41'

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)

        self.report = self.client.get_report(code=self.SPECIFIC_REPORT_CODE)
    
    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()
    
    def test_invalid_report(self) -> None:
        '''
        The client should raise an exception when attempting to fetch data from a nonexistent report.

        Preferably GQL should raise this error as it will likely include
        better information than the client could easily produce.
        '''
        with self.assertRaises(Exception):
            # Since the client is lazy we must attempt to access some data first
            report = self.client.get_report(code='thisdoesnotexist')
            report.zone()

    def test_master_data(self) -> None:
        '''
        The client should be able to fetch master data about the report.
        '''
        self.assertIsNotNone(self.report.log_version())
        self.assertEqual(self.report.log_version(), 53)

        self.assertGreater(len(self.report.actors()), 0)
        self.assertEqual(self.report.actors()[0].name, 'Environment')

        self.assertGreater(len(self.report.abilities()), 0)
        self.assertEqual(self.report.abilities()[0].game_id, 0)
    
    def test_fields(self) -> None:
        '''
        The client should be able to fetch the report's fields.
        '''
        self.assertEqual(self.report.title(), 'Abyssos')
        self.assertEqual(self.report.start_time(), 1662771478876)
        self.assertEqual(self.report.end_time(), 1662781027781)
        self.assertEqual(self.report.segments(), 13)
        # exported segments, revision, visibility is not implemented
    
    def test_fight(self) -> None:
        '''
        The client should be able to access individual fights through a report.
        '''
        self.assertIsInstance(self.report.fight(), FFLogsFight)
        for fight in self.report.fights():
            self.assertIsInstance(fight, FFLogsFight)

class ReportPageTest(unittest.TestCase):
    '''
    Tests for pages of a guild's reports.

    This test cases makes assumptions on the availability of a guild/user.
    If the tests break, it may be because visibility settings were changed or the guild/user was deleted.
    '''

    SPECIFIC_GUILD = 81924
    SPECIFIC_USER = 315987

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
    
    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_guild_reports_pagination(self) -> None:
        '''
        The client should be able to handle pagination of guild reports
        '''
        report_pages = self.client.report_pages({'guildID': self.SPECIFIC_GUILD})

        page_one = report_pages.__next__()
        self.assertIsInstance(page_one, FFLogsReportPage)

        report_one = page_one.__iter__().__next__()
        self.assertIsInstance(report_one, FFLogsReport)

    def test_user_reports_pagination(self) -> None:
        '''
        The client should be able to handle pagination of user reports
        '''
        report_pages = self.client.report_pages({'userID': self.SPECIFIC_USER})

        page_one = report_pages.__next__()
        self.assertIsInstance(page_one, FFLogsReportPage)

        report_one = page_one.__iter__().__next__()
        self.assertIsInstance(report_one, FFLogsReport)


if __name__ == '__main__':
    unittest.main()
