import unittest

from fflogsapi.characters.character import FFLogsCharacter
from fflogsapi.client import FFLogsClient
from fflogsapi.data import FFLogsReportTag
from fflogsapi.reports.fight import FFLogsFight
from fflogsapi.reports.pages import FFLogsReportPage
from fflogsapi.reports.report import FFLogsReport
from fflogsapi.world.region import FFLogsRegion
from fflogsapi.world.zone import FFLogsZone

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class ReportTest(unittest.TestCase):
    '''
    Test cases for FF Logs reports.

    This test case makes assumptions on the availability of a specific report.
    If the tests break, it may be because visibility settings
    were changed or the report was deleted.
    '''

    SPECIFIC_REPORT_CODE = '2Kf9y6wzanWkBJ41'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.report = cls.client.get_report(code=cls.SPECIFIC_REPORT_CODE)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_invalid_report(self) -> None:
        '''
        The client should raise an exception when attempting
        to fetch data from a nonexistent report.

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

        actors = self.report.actors()
        self.assertGreater(len(actors), 0)
        self.assertIn('Milotiq Umida', [actor.name for actor in actors])

        specific_actor = self.report.actor(id=actors[0].id)
        self.assertEqual(specific_actor.id, actors[0].id)

        abilities = self.report.abilities()
        self.assertGreater(len(abilities), 0)
        ability_ids = [ability.game_id for ability in abilities]
        self.assertIn(0, ability_ids)

    def test_archivation_data(self) -> None:
        '''
        The client should be able to get archivation data from a report.
        '''
        archivation = self.report.archivation_data()
        self.assertEqual(archivation.archived, True)
        self.assertEqual(archivation.accessible, False)
        self.assertEqual(archivation.date, 1725939433)

    def test_zone(self) -> None:
        '''
        The client should be able to get the *primary* zone of the report
        '''
        zone = self.report.zone()
        self.assertIsInstance(zone, FFLogsZone)
        self.assertEqual(zone.id, 49)

    def test_fields(self) -> None:
        '''
        The client should be able to fetch the report's fields.
        '''
        self.assertEqual(self.report.title(), 'Abyssos')
        self.assertEqual(self.report.start_time(), 1662771478876)
        self.assertEqual(self.report.end_time(), 1662781027781)
        self.assertEqual(self.report.duration(), 1662781027781 - 1662771478876)
        self.assertEqual(self.report.segments(), 13)
        self.assertEqual(self.report.exported_segments(), 13)
        self.assertEqual(self.report.revision(), 12)
        self.assertEqual(self.report.visibility(), 'public')

    def test_fights(self) -> None:
        '''
        The client should be able to access individual fights through a report.
        '''
        last_fight = self.report.fight()
        self.assertIsInstance(last_fight, FFLogsFight)

        for fight in self.report.fights():
            self.assertIsInstance(fight, FFLogsFight)

        for fight in self.report:
            self.assertIsInstance(last_fight, FFLogsFight)

    def test_nonexistent_fight(self) -> None:
        '''
        The client should return None when requesting a fight that does not exist.
        '''
        fake_fight = self.report.fight(id=123456789)
        self.assertIsNone(fake_fight)

    def test_guild(self) -> None:
        '''
        The client should be able to fetch the guild this report belongs to.

        It should return None for a personal log report.
        '''
        guild = self.report.guild()
        self.assertEqual(guild.id, 81924)
        self.assertEqual(guild.name(), 'Kindred')

        personal_report = self.client.get_report(code='BWgAdkachXJ3Drj9')
        guild = personal_report.guild()
        self.assertIsNone(guild)

    def test_tag(self) -> None:
        '''
        The client should be able to get the tag of a report.
        '''
        tag = self.report.tag()
        self.assertIsNone(tag)

        report = self.client.get_report(code='MzDWYXrxRZ6L3BN4')
        tag = report.tag()
        self.assertIsInstance(tag, FFLogsReportTag)
        self.assertEqual(tag.name, 'LB3 it bro')

    def test_owner(self) -> None:
        '''
        The client should be able to fetch the user that owns the report.
        '''
        owner = self.report.owner()
        self.assertEqual(owner.id, 315987)
        self.assertEqual(owner.name(), 'Peridise')

    def test_region(self) -> None:
        '''
        The client should be able to fetch the region of the report.
        '''
        region = self.report.region()
        self.assertIsInstance(region, FFLogsRegion)
        self.assertEqual(region.id, 1)

    def test_ranked_characters(self) -> None:
        '''
        The client should be able to get a list of all characters that ranked in the report.
        '''
        characters = self.report.ranked_characters()
        self.assertEqual(len(characters), 16)
        for character in characters:
            self.assertIsInstance(character, FFLogsCharacter)


class ReportPageTest(unittest.TestCase):
    '''
    Tests for pages of a guild's reports.

    This test cases makes assumptions on the availability of a guild/user.
    If the tests break, it may be because visibility settings
    were changed or the guild/user was deleted.
    '''

    GUILD_ID = 81924
    USER_ID = 315987

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)

    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_guild_reports_pagination(self) -> None:
        '''
        The client should be able to handle pagination of guild reports
        '''
        report_pages = self.client.reports({'guildID': self.GUILD_ID})

        page_one = report_pages.__next__()
        self.assertIsInstance(page_one, FFLogsReportPage)

        report_one = page_one.__iter__().__next__()
        self.assertIsInstance(report_one, FFLogsReport)

    def test_user_reports_pagination(self) -> None:
        '''
        The client should be able to handle pagination of user reports
        '''
        report_pages = self.client.reports({'userID': self.USER_ID})

        page_one = report_pages.__next__()
        self.assertIsInstance(page_one, FFLogsReportPage)

        report_one = page_one.__iter__().__next__()
        self.assertIsInstance(report_one, FFLogsReport)


if __name__ == '__main__':
    unittest.main()
