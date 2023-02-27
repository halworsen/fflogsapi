import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.constants import FIGHT_DIFFICULTY_SAVAGE
from fflogsapi.util.gql_enums import GQLEnum
from fflogsapi.world.server import FFLogsServer

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class CharacterTest(unittest.TestCase):
    '''
    Test cases for FFLogs characters.

    This test case makes assumptions on the availability of a specific character.
    If the tests break, it may be because visibility settings
    were changed or the character was deleted.
    '''

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.character = cls.client.get_character(id=19181640)
        cls.named_character = cls.client.get_character(filters={
            'name': 'Dylan Kusarigama',
            'serverRegion': 'EU',
            'serverSlug': 'Lich',
        })

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_specific_character(self) -> None:
        '''
        The client should be able to find a character both by ID and filter fields.
        '''
        self.assertEqual(self.character.id(), self.named_character.id())

    def test_fields(self) -> None:
        '''
        The client should be able to fetch fields about the character
        such as their name, server, etc.
        '''
        self.assertEqual(self.character.name(), 'Dylan Kusarigama')
        self.assertIsInstance(self.character.server(), FFLogsServer)
        self.assertEqual(self.character.lodestone_id(), 28321575)
        # considering these as volatile. there is no point in testing for specific values
        self.assertIsInstance(self.character.fc_rank(), int)
        self.assertIsInstance(self.character.hidden(), bool)

    def test_encounter_rankings(self) -> None:
        '''
        The client should be able to fetch encounter ranking information about the character.
        '''
        rankings = self.character.encounter_rankings(filters={
            'encounterID': 87,
            'specName': 'Reaper',
            'difficulty': FIGHT_DIFFICULTY_SAVAGE,
        })
        self.assertIsInstance(rankings, dict)
        self.assertEqual(rankings['difficulty'], FIGHT_DIFFICULTY_SAVAGE)

    def test_zone_rankings(self) -> None:
        '''
        The client should be able to fetch zone ranking information about the character.
        '''
        rankings = self.character.zone_rankings(filters={
            'zoneID': 49,
            'specName': 'Reaper',
            'metric': GQLEnum('rdps'),
        })
        self.assertIsInstance(rankings, dict)
        self.assertEqual(rankings['difficulty'], FIGHT_DIFFICULTY_SAVAGE)

    def test_game_data(self) -> None:
        '''
        The client should be able to fetch game data about the character.
        '''
        game_data = self.character.game_data(filters={'forceUpdate': True})
        self.assertIsInstance(game_data, dict)


if __name__ == '__main__':
    unittest.main()
