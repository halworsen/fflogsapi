import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.constants import FightDifficulty, PartySize
from fflogsapi.reports.dataclasses import (FFLogsActor, FFLogsReportCharacterRanking,
                                           FFLogsReportComboRanking, FFLogsReportRanking,)
from fflogsapi.util.gql_enums import GQLEnum
from fflogsapi.world.encounter import FFLogsEncounter

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class FightTest(unittest.TestCase):
    '''
    Test cases for FF Logs fights.

    This test case makes assumptions on the availability of a specific report.
    If the tests break, it may be because visibility settings
    were changed or the report was deleted.
    '''

    SPECIFIC_REPORT_CODE = '2Kf9y6wzanWkBJ41'
    SPECIFIC_FIGHT_ID = 15

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.report = cls.client.get_report(code=cls.SPECIFIC_REPORT_CODE)
        cls.fight = cls.report.fight(id=cls.SPECIFIC_FIGHT_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_fields(self) -> None:
        '''
        The client should be able to fetch fields about the fight
        such as the difficulty, boss name, etc.
        '''
        self.assertEqual(self.fight.name(), 'Hephaistos II')
        self.assertIsInstance(self.fight.encounter(), FFLogsEncounter)
        self.assertEqual(self.fight.encounter().id(), 87)
        self.assertEqual(self.fight.difficulty(), FightDifficulty.SAVAGE.value)
        self.assertEqual(self.fight.size(), PartySize.FULL.value)
        self.assertEqual(self.fight.fight_percentage(), 55.93)
        self.assertEqual(self.fight.percentage(), 55.93)
        self.assertEqual(self.fight.start_time(), 8224400)
        self.assertEqual(self.fight.end_time(), 8500006)
        self.assertEqual(self.fight.in_progress(), False)
        self.assertEqual(self.fight.is_kill(), False)
        self.assertEqual(self.fight.has_echo(), False)
        self.assertEqual(self.fight.standard_comp(), True)

        self.assertTupleEqual(
            self.fight.bounding_box(),
            (8000, 7700, 12000, 11934),
        )

        self.assertListEqual(
            sorted(self.fight.friendly_players()),
            sorted([126, 125, 124, 91, 123, 38, 130, 129, 160]),
        )

    def test_events(self) -> None:
        '''
        The client should be able to fetch events that occured in a fight
        '''
        events = self.fight.events({
            'sourceAurasAbsent': 'Medicated',
            'dataType': GQLEnum('Deaths'),
        })

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 8)

    def test_graph(self) -> None:
        '''
        The client should be able to fetch graphs from fights
        '''
        graph = self.fight.graph({
            'dataType': GQLEnum('DamageDone'),
            'sourceAurasPresent': 'Medicated',
        })

        self.assertIsNotNone(graph)
        self.assertDictEqual(graph['downtime'][0], {
            'startTime': 8343649,
            'endTime': 8384962
        })
        self.assertAlmostEqual(graph['series'][0]['pointInterval'], 1148.3583333333333, places=4)
        # +1 for total damage
        self.assertEqual(len(graph['series']), PartySize.FULL.value + 1)

        count_data = list(filter(lambda d: d['name'] == 'The Count', graph['series']))[0]
        self.assertEqual(count_data['name'], 'The Count')
        self.assertEqual(count_data['total'], 1050501)

    def test_table(self) -> None:
        '''
        The client should be able to fetch table information from the fight
        '''
        table = self.fight.table({
            'dataType': GQLEnum('Casts'),
            'abilityID': 7535,
        })

        self.assertIsNotNone(table)
        self.assertEqual(len(table['entries']), 2)
        self.assertEqual(table['downtime'], 41313)
        self.assertEqual(table['entries'][0]['hitCount'], 3)

    def test_invalid_times(self) -> None:
        '''
        A fight should not allow you to fetch events before the fight has started
        or after it has ended.
        '''
        with self.assertRaises(ValueError):
            self.fight.events({
                'startTime': self.fight.start_time() - 1,
                'sourceAurasAbsent': 'Medicated',
                'dataType': GQLEnum('Deaths'),
            })

        with self.assertRaises(ValueError):
            self.fight.events({
                'endTime': self.fight.end_time() + 1,
                'sourceAurasAbsent': 'Medicated',
                'dataType': GQLEnum('Deaths'),
            })

    def test_rankings(self) -> None:
        '''
        The client should be able to fetch ranking information from a fight
        '''
        # the common/reusable fight is a wipe, and should not have rankings
        self.assertIsNone(self.fight.rankings())

        # get rankings from an actual kill
        rankings = self.report.fight(id=17).rankings(metric='rdps')
        self.assertIsInstance(rankings, FFLogsReportRanking)

        self.assertEqual(rankings.patch, 6.2)
        self.assertEqual(rankings.deaths, 1)

        self.assertGreater(len(rankings.character_rankings), 0)
        self.assertGreater(len(rankings.combo_rankings), 0)
        self.assertIsInstance(rankings.character_rankings[0], FFLogsReportCharacterRanking)
        self.assertIsInstance(rankings.combo_rankings[0], FFLogsReportComboRanking)

        gunbreaker = list(filter(
            lambda r: r.job.name == 'Gunbreaker',
            rankings.character_rankings
        ))[0]
        self.assertAlmostEqual(gunbreaker.amount, 6491.9, places=1)

        healers = list(filter(
            lambda r: r.type == 'healers',
            rankings.combo_rankings
        ))[0]
        self.assertAlmostEqual(healers.amount, 9793.7, places=1)

    def test_multiple_event_pages(self) -> None:
        '''
        A fight should seamlessly combine multiple pages of fight events
        '''
        report = self.client.get_report('fZ7XKA6gyzDY43Nd')
        kill_fight = report.fight(id=8)
        events = kill_fight.events(filters={
            'dataType': GQLEnum('Casts'),
            'useAbilityIDs': True,
        })
        self.assertIsInstance(events, list)
        self.assertIsInstance(events[0], dict)
        self.assertEqual(events[0]['type'], 'cast')

    def test_player_details(self) -> None:
        '''
        The client should be able to fetch player details for a fight
        '''
        details = self.fight.player_details()
        self.assertGreater(len(details), 0)

        surana = list(filter(
            lambda d: d.id == 160,
            details,
        ))[0]
        self.assertEqual(surana.name, 'Surana Crescence')
        self.assertIsInstance(surana.actor, FFLogsActor)
        self.assertEqual(surana.job.name, 'Dancer')
        self.assertEqual(surana.server, 'Gilgamesh')

    def test_npcs(self) -> None:
        '''
        The client should be able to get both enemy and friendly NPCs from a fight.
        '''
        enemies = self.fight.enemy_npcs()
        specific_enemy = list(filter(
            lambda e: e.id == 41,
            enemies,
        ))[0]

        self.assertEqual(specific_enemy.actor.name, 'Hephaistos')
        self.assertEqual(specific_enemy.hostile, True)

        friends = self.fight.friendly_npcs()
        # :(
        self.assertIsNone(friends)

        dsu_report = self.client.get_report(code='Tpx4NKYMQz1rDVbX')
        fight = dsu_report.fight(id=7)
        friends = fight.friendly_npcs()
        haurchefant = list(filter(
            lambda e: e.id == 21,
            friends,
        ))[0]
        self.assertEqual(haurchefant.instance_count, 3)
        self.assertEqual(haurchefant.actor.name, 'Haurchefant')

    def test_pets(self) -> None:
        '''
        The client should be able to get a list of friendly pets from a fight.
        '''
        pets = self.fight.pets()
        bunshin = list(filter(
            lambda p: p.id == 133,
            pets,
        ))[0]

        self.assertEqual(bunshin.instance_count, 3)
        self.assertEqual(bunshin.pet_owner.name, 'Riksa Ui')

    def test_game_zone(self) -> None:
        '''
        The client should be able to get the game zone a fight took place in.
        '''
        zone = self.fight.game_zone()
        self.assertEqual(zone.id, 1088)
        self.assertEqual(zone.name, 'Stygian Insenescence Cells')

    def test_maps(self) -> None:
        '''
        The client should be able to get the maps a fight took place in.
        '''
        maps = self.fight.maps()
        self.assertEqual(len(maps), 1)
        self.assertEqual(maps[0].id, 808)
        self.assertEqual(maps[0].name, 'Stygian Insenescence Cells')

    def test_phases(self) -> None:
        '''
        The client should be able to get phase information from fights containing multiple phases
        '''
        report = self.client.get_report(code='6HQYx9jA8mbC4VF1')
        # exam time
        # (fight id, last phase, last phase abs, last phase is intermission)
        answer_key = [
            (3, 2, 3, True), (5, 3, 4, False), (9, 2, 2, False),
            (13, 1, 1, True), (24, 4, 5, False),
        ]

        for key in answer_key:
            fight = report.fight(id=key[0])
            answer = (
                key[0],
                fight.last_phase(),
                fight.last_phase_absolute(),
                fight.last_phase_intermission(),
            )

            self.assertTupleEqual(answer, key)


if __name__ == '__main__':
    unittest.main()
