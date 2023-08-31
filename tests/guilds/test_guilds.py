import unittest

from fflogsapi.characters.character import FFLogsCharacter
from fflogsapi.client import FFLogsClient
from fflogsapi.data import (FFLogsAttendanceReport, FFLogsGuildZoneRankings,
                                          FFLogsRank, FFLogsReportTag,)
from fflogsapi.guilds.guild import FFLogsGuild
from fflogsapi.guilds.pages import (FFLogsGuildAttendancePaginationIterator, FFLogsGuildPage,
                                    FFLogsGuildPaginationIterator,)
from fflogsapi.reports.report import FFLogsReport
from fflogsapi.world.server import FFLogsServer
from fflogsapi.world.zone import FFLogsZone

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class FightTest(unittest.TestCase):
    '''
    Test cases for FFLogs fights.

    This test case makes assumptions on the availability of a specific report.
    If the tests break, it may be because visibility settings
    were changed or the report was deleted.
    '''

    GUILD_ID = 81924  # Kindred

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.guild = cls.client.get_guild(id=cls.GUILD_ID)
        cls.named_guild = cls.client.get_guild(filters={
            'name': 'Kindred',
            'serverRegion': 'NA',
            'serverSlug': 'Gilgamesh',
        })

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_specific_guild(self) -> None:
        '''
        The client should be able to find a guild both by ID and filter fields.
        '''
        self.assertEqual(self.guild.id, self.named_guild.id)

    def test_guild_pages(self) -> None:
        '''
        The client should be able to get a pagination of all guilds on the site.
        '''
        guild_pages = self.client.guilds(filters={
            'serverRegion': 'EU',
        })
        self.assertIsInstance(guild_pages, FFLogsGuildPaginationIterator)
        first_page = guild_pages.__next__()
        self.assertIsInstance(first_page, FFLogsGuildPage)

        guild = first_page.__iter__().__next__()
        self.assertIsInstance(guild, FFLogsGuild)

    def test_fields(self) -> None:
        '''
        The client should be able to fetch fields about the guild
        such as its name, server, faction, etc.
        '''
        self.assertEqual(self.guild.id, self.GUILD_ID)
        self.assertEqual(self.guild.name(), 'Kindred')
        self.assertEqual(self.guild.description(), 'It\'s lit')
        self.assertIsInstance(self.guild.server(), FFLogsServer)
        self.assertEqual(self.guild.server().name(), 'Gilgamesh')
        self.assertEqual(self.guild.type(), '1')

        self.assertEqual(self.guild.grand_company().name, 'The Immortal Flames')

        self.assertEqual(self.guild.competition_mode(), True)
        self.assertEqual(self.guild.stealth_mode(), False)

    def test_current_rank(self) -> None:
        '''
        The client should raise an error when trying to get the user's current rank while in
        client mode.

        See the user tests for an explanation for why this isn't being tested in user mode.
        '''
        with self.assertRaises(Exception):
            self.guild.current_rank()

    def test_members(self) -> None:
        '''
        The client should be able to get the characters belonging to the guild.
        '''
        characters = self.guild.characters()
        first_page = characters.__next__()
        first_char = first_page.__iter__().__next__()
        self.assertEqual(len(first_page), 15)

        self.assertIsInstance(first_char, FFLogsCharacter)

    def test_tags(self) -> None:
        '''
        The client should be able to get a guild's report tags.
        '''
        guild = self.client.get_guild(id=98575)
        tags = guild.tags()
        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 1)
        self.assertIsInstance(tags[0], FFLogsReportTag)
        self.assertEqual(tags[0].name, 'LB3 it bro')

    def test_attendance(self) -> None:
        '''
        The client should be able to get a guild's attendance reports.
        '''
        zone_id = 53  # TOP
        attendance = self.guild.attendance(filters={
            'zoneID': zone_id,  # TOP
        })
        self.assertIsInstance(attendance, FFLogsGuildAttendancePaginationIterator)
        first_page = attendance.__next__()
        reports: list[FFLogsAttendanceReport] = list(first_page)

        report_code = 'ZPJRCapzfvrH9F23'
        matching_report: FFLogsAttendanceReport = None
        for report in reports:
            self.assertIsInstance(report, FFLogsAttendanceReport)
            if report.report.code == report_code:
                matching_report = report
                break
        self.assertIsNotNone(matching_report)

        self.assertIsInstance(matching_report.report, FFLogsReport)
        self.assertEqual(matching_report.report.code, report_code)

        self.assertIsInstance(matching_report.zone, FFLogsZone)
        self.assertEqual(matching_report.zone.id, zone_id)

        self.assertEqual(matching_report.start, 1677808649812)

        self.assertIsInstance(matching_report.players, list)
        for player in matching_report.players:
            self.assertIsInstance(player, tuple)
            self.assertIsInstance(player[0], str)
            self.assertIsInstance(player[1], int)
            self.assertIsInstance(player[2], str)

    def test_rankings(self) -> None:
        '''
        The client should be able to get zone ranking information about a guild.

        This is pretty volatile so just do type checking
        '''
        rankings = self.guild.zone_rankings(zone=53)
        self.assertIsInstance(rankings, FFLogsGuildZoneRankings)
        self.assertIsNone(rankings.completion_speed)
        self.assertIsNone(rankings.speed)
        self.assertIsInstance(rankings.progress, tuple)

        for rank in rankings.progress:
            self.assertIsInstance(rank, FFLogsRank)
        world = rankings.progress[0]
        self.assertIsNone(world.percentile)
        self.assertIsInstance(world.color, str)
        self.assertIsInstance(world.number, int)

        # same thing but use a FFLogsZone instead
        zone = self.client.get_zone(id=53)
        rankings = self.guild.zone_rankings(zone=zone)
        self.assertIsInstance(rankings, FFLogsGuildZoneRankings)
        self.assertIsNone(rankings.completion_speed)
        self.assertIsNone(rankings.speed)
        self.assertIsInstance(rankings.progress, tuple)

        for rank in rankings.progress:
            self.assertIsInstance(rank, FFLogsRank)
        world = rankings.progress[0]
        self.assertIsNone(world.percentile)
        self.assertIsInstance(world.color, str)
        self.assertIsInstance(world.number, int)


if __name__ == '__main__':
    unittest.main()
