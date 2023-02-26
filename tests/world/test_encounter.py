import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.constants import PARTY_SIZE_FULL_PARTY
from fflogsapi.util.gql_enums import GQLEnum
from fflogsapi.world.zone import FFLogsZone

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class EncounterTest(unittest.TestCase):
    '''
    Test cases for FFLogs encounter information.
    '''

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        # hephaistos 2 has id 87
        self.encounter = self.client.get_encounter(id=87)

    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_fields(self) -> None:
        '''
        The client should be able to fetch simple fields from the encounter
        '''
        self.assertEqual(self.encounter.id(), 87)
        self.assertEqual(self.encounter.name(), 'Hephaistos II')

    def test_character_rankings(self) -> None:
        '''
        The client should be able to fetch information about an encounter's character rankings.
        '''
        char_rankings = self.encounter.character_rankings({
            'page': 1,
            'serverRegion': 'EU',
            'serverSlug': 'Twintania',
            'specName': 'Dancer',
            'metric': GQLEnum('rdps'),
        })

        self.assertIsNotNone(char_rankings)
        self.assertEqual(char_rankings['rankings'][0]['spec'], 'Dancer')

    def test_fight_rankings(self) -> None:
        '''
        The client should be able to fetch information about fight rankings.
        '''
        fight_rankings = self.encounter.fight_rankings({
            'page': 1,
            'serverRegion': 'NA',
            'metric': GQLEnum('execution')
        })

        self.assertIsNotNone(fight_rankings)
        # i will bite my fingers off if a group with <8 players made it to top execution rankings
        self.assertEqual(fight_rankings['rankings'][0]['size'], PARTY_SIZE_FULL_PARTY)

    def test_zone(self) -> None:
        '''
        The client should be able to provide a zone in which an encounter takes place.
        '''
        self.assertIsInstance(self.encounter.zone(), FFLogsZone)


if __name__ == '__main__':
    unittest.main()
