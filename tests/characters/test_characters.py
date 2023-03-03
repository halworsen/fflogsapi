import unittest

from fflogsapi.characters.character import FFLogsCharacter
from fflogsapi.characters.pages import FFLogsCharacterPage
from fflogsapi.client import FFLogsClient
from fflogsapi.constants import FIGHT_DIFFICULTY_SAVAGE
from fflogsapi.guilds.guild import FFLogsGuild
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

    CHARACTER_ID = 19181640
    CHARACTER_NAME = 'Dylan Kusarigama'

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.character = cls.client.get_character(id=cls.CHARACTER_ID)
        cls.named_character = cls.client.get_character(filters={
            'name': cls.CHARACTER_NAME,
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
        self.assertEqual(self.character.id(), self.CHARACTER_ID)
        self.assertEqual(self.character.name(), self.CHARACTER_NAME)
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

    def test_guilds(self) -> None:
        '''
        The client should be able to fetch a list of all guilds the character belongs to.
        '''
        # get a character that actually belongs to a guild
        surana = self.client.get_character(id=18994677)
        guilds = surana.guilds()
        self.assertIsInstance(guilds[0], FFLogsGuild)
        self.assertEqual(guilds[0].id(), 110310)

    def test_game_data(self) -> None:
        '''
        The client should be able to fetch game data about the character.
        '''
        game_data = self.character.game_data(filters={'forceUpdate': True})
        self.assertIsInstance(game_data, dict)

    def test_character_pagination(self) -> None:
        '''
        The client should be able to fetch a pagination of characters belonging to a guild.
        '''
        character_pages = self.client.character_pages(guild_id=111093)
        for page in character_pages:
            self.assertIsInstance(page, FFLogsCharacterPage)
            for character in page:
                self.assertIsInstance(character, FFLogsCharacter)


if __name__ == '__main__':
    unittest.main()
