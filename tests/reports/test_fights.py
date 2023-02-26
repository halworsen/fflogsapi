import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.util.gql_enums import GQLEnum
from fflogsapi.constants import FIGHT_DIFFICULTY_SAVAGE, PARTY_SIZE_FULL_PARTY
from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET

class FightTest(unittest.TestCase):
    '''
    Test cases for FFLogs fights.

    This test case makes assumptions on the availability of a specific report.
    If the tests break, it may be because visibility settings were changed or the report was deleted.
    '''

    SPECIFIC_REPORT_CODE = '2Kf9y6wzanWkBJ41'
    SPECIFIC_FIGHT_ID = 15

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        report = self.client.get_report(code=self.SPECIFIC_REPORT_CODE)
        self.fight = report.fight(id=self.SPECIFIC_FIGHT_ID)
    
    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_fields(self) -> None:
        '''
        The client should be able to fetch fields about the fight such as the difficulty, boss name, etc.
        '''
        self.assertEqual(self.fight.name(), "Hephaistos II")

        self.assertEqual(self.fight.encounter_id(), 87)
        self.assertEqual(self.fight.difficulty(), FIGHT_DIFFICULTY_SAVAGE)
        self.assertEqual(self.fight.size(), PARTY_SIZE_FULL_PARTY)
        self.assertEqual(self.fight.fight_percentage(), 55.93)
        self.assertEqual(self.fight.percentage(), 55.93)
        self.assertEqual(self.fight.start_time(), 8224400)
        self.assertEqual(self.fight.end_time(), 8500006)

        self.assertEqual(self.fight.is_kill(), False)
        self.assertEqual(self.fight.has_echo(), False)
        self.assertEqual(self.fight.standard_comp(), True)

        self.assertListEqual(
            self.fight.friendly_players(),
            [126, 125, 124, 91, 123, 38, 130, 129, 160],
        )
    
    def test_events(self) -> None:
        '''
        The client should be able to fetch events that occured in a fight
        '''
        events = self.fight.fight_events({
            'sourceAurasAbsent': 'Medicated',
            'dataType': GQLEnum('Deaths'),
        })

        self.assertIsNotNone(events)
        self.assertEqual(len(events), 8)

    def test_graph(self) -> None:
        '''
        The client should be able to fetch graphs from fights
        '''
        graph = self.fight.fight_graph({
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
        self.assertEqual(len(graph['series']), PARTY_SIZE_FULL_PARTY + 1)
        self.assertEqual(graph['series'][2]['name'], 'The Count')
        self.assertEqual(graph['series'][2]['total'], 1050501)
    
    def test_table(self) -> None:
        '''
        The client should be able to fetch table information from the fight
        '''
        table = self.fight.fight_table({
            'dataType': GQLEnum('Casts'),
            'abilityID': 7535,
        })

        self.assertIsNotNone(table)
        self.assertEqual(len(table['entries']), 2)
        self.assertEqual(table['downtime'], 41313)
        self.assertEqual(table['entries'][0]['hitCount'], 3)


if __name__ == '__main__':
    unittest.main()
