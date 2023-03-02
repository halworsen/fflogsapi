import unittest

from fflogsapi.client import FFLogsClient

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class ProgressRaceTest(unittest.TestCase):
    '''
    Test cases for FF Logs progression races.
    '''

    ZONE_ID = 53  # TOP
    GUILD_ID = 100030  # Neverland

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(
            CLIENT_ID,
            CLIENT_SECRET,
            cache_expiry=CACHE_EXPIRY,
        )
        cls.race_data = cls.client.get_progress_race(
            filters={'zoneID': cls.ZONE_ID, 'guildID': cls.GUILD_ID},
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_race_data(self) -> None:
        '''
        The client should be able to fetch information about progress races.
        '''
        neverland = self.race_data[0]
        encounter = neverland['encounters'][0]
        self.assertEqual(neverland['id'], self.GUILD_ID)
        self.assertEqual(encounter['name'], 'The Omega Protocol')


if __name__ == '__main__':
    unittest.main()
