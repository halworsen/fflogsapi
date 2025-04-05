import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.constants import FightDifficulty, PartySize
from fflogsapi.data import (FFLogsActor, FFLogsReportCharacterRanking, FFLogsReportComboRanking,
                            FFLogsReportRanking,)
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

    SPECIFIC_REPORT_CODE = 'LwdbchzWYPZxHDRt'
    SPECIFIC_FIGHT_ID = 14

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
        self.assertEqual(self.fight.name(), 'Wicked Thunder')
        self.assertIsInstance(self.fight.encounter(), FFLogsEncounter)
        self.assertEqual(self.fight.encounter().id, 96)
        self.assertEqual(self.fight.difficulty(), FightDifficulty.SAVAGE.value)
        self.assertEqual(self.fight.size(), PartySize.FULL.value)
        self.assertEqual(self.fight.fight_percentage(), 48.51)
        self.assertEqual(self.fight.percentage(), 48.51)
        self.assertEqual(self.fight.start_time(), 5582056)
        self.assertEqual(self.fight.end_time(), 5957574)
        self.assertEqual(self.fight.in_progress(), False)
        self.assertEqual(self.fight.is_kill(), False)
        self.assertEqual(self.fight.has_echo(), False)
        self.assertEqual(self.fight.standard_comp(), True)

        self.assertTupleEqual(
            self.fight.bounding_box(),
            (8000, 7997, 12000, 11839),
        )

        self.assertListEqual(
            sorted(self.fight.friendly_players()),
            sorted([111, 110, 109, 108, 106, 114, 113, 112, 32]),
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
        self.assertEqual(len(events), 10)

    def test_graph(self) -> None:
        '''
        The client should be able to fetch graphs from fights
        '''
        graph = self.fight.graph({
            'dataType': GQLEnum('DamageDone'),
            'sourceAurasPresent': 'Medicated',
        })

        self.assertIsNotNone(graph)
        self.assertEqual(graph['startTime'], self.fight.start_time())
        self.assertEqual(graph['endTime'], self.fight.end_time())
        self.assertAlmostEqual(graph['series'][0]['pointInterval'], 1564.6583333333333, places=4)
        # +1 for total damage
        self.assertEqual(len(graph['series']), PartySize.FULL.value + 1)

        player_data = list(filter(lambda d: d['name'] == 'Reks Rotari', graph['series']))[0]
        self.assertEqual(player_data['name'], 'Reks Rotari')
        self.assertEqual(player_data['total'], 8854424)

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
        self.assertEqual(table['entries'][0]['hitCount'], 2)

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
        rankings = self.report.fight(id=16).rankings(metric='rdps')
        self.assertIsInstance(rankings, FFLogsReportRanking)

        self.assertEqual(rankings.patch, 7.1)
        self.assertEqual(rankings.deaths, 0)

        self.assertGreater(len(rankings.character_rankings), 0)
        self.assertGreater(len(rankings.combo_rankings), 0)
        self.assertIsInstance(rankings.character_rankings[0], FFLogsReportCharacterRanking)
        self.assertIsInstance(rankings.combo_rankings[0], FFLogsReportComboRanking)

        ranking = list(filter(
            lambda r: r.job.name == 'Paladin',
            rankings.character_rankings
        ))[0]
        self.assertAlmostEqual(ranking.amount, 17590, places=1)

        healers = list(filter(
            lambda r: r.type == 'healers',
            rankings.combo_rankings
        ))[0]
        self.assertAlmostEqual(healers.amount, 29240, places=1)

    def test_multiple_event_pages(self) -> None:
        '''
        A fight should seamlessly combine multiple pages of fight events
        '''
        report = self.client.get_report('tgFNX14HGLBfWaCk')
        kill_fight = report.fight(id=2)
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

        player = list(filter(
            lambda d: d.id == 111,
            details,
        ))[0]
        self.assertEqual(player.name, 'Reks Rotari')
        self.assertIsInstance(player.actor, FFLogsActor)
        self.assertEqual(player.job.name, 'Reaper')
        self.assertEqual(player.server, 'Shiva')

    def test_npcs(self) -> None:
        '''
        The client should be able to get both enemy and friendly NPCs from a fight.
        '''
        enemies = self.fight.enemy_npcs()
        specific_enemy = list(filter(
            lambda e: e.id == 144,
            enemies,
        ))[0]

        self.assertEqual(specific_enemy.actor.name, 'Wicked Thunder')
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
        pet = list(filter(
            lambda p: p.id == 115,
            pets,
        ))[0]

        self.assertEqual(pet.instance_count, 4)
        self.assertEqual(pet.pet_owner.name, 'Thia Huntington')

    def test_game_zone(self) -> None:
        '''
        The client should be able to get the game zone a fight took place in.
        '''
        zone = self.fight.game_zone()
        self.assertEqual(zone.id, 1232)
        self.assertEqual(zone.name, 'The Thundering')

    def test_maps(self) -> None:
        '''
        The client should be able to get the maps a fight took place in.
        '''
        maps = self.fight.maps()
        self.assertEqual(len(maps), 1)
        self.assertEqual(maps[0].id, 924)
        self.assertEqual(maps[0].name, 'The Thundering')

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
                fight.last_phase(as_dataclass=True).id,
                fight.last_phase_absolute(),
                fight.last_phase_intermission(),
            )

            self.assertTupleEqual(answer, key)

        # test phase information
        report = self.client.get_report(code='cLxvtB7HAnQT9zVh')
        top_wipe = report.fight(id=20)
        dsu_wipe = report.fight(id=35)
        ucob_kill = report.fight(id=48)

        self.assertEqual(top_wipe.last_phase(as_dataclass=True).name, 'P3: Omega Reconfigured')
        # this is a weird quirk of the API but it is how it behaves
        self.assertEqual(
            dsu_wipe.last_phase(as_dataclass=True).name,
            'P1: Adelphel, Grinnaux and Charibert'
        )
        self.assertEqual(
            dsu_wipe.last_phase(
                ignore_intermissions=False,
                as_dataclass=True
            ).name,
            'Intermission: Rewind!'
        )
        ucob_phases = ucob_kill.phases()
        self.assertEqual(len(ucob_phases), 5)
        self.assertEqual(ucob_phases[2].name, 'P3: Bahamut Prime')


if __name__ == '__main__':
    unittest.main()
