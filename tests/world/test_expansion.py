import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.world.expansion import FFLogsExpansion
from fflogsapi.world.zone import FFLogsZone

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class ExpansionTest(unittest.TestCase):
    '''
    Test cases for FF Logs expansion information.
    '''

    EXPAC_ID = 3  # shadowbringers

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.expansion = cls.client.get_expansion(id=cls.EXPAC_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_fields(self) -> None:
        '''
        The client should be able to fetch the id and name of the expansion.
        '''
        self.assertEqual(self.expansion.id(), self.EXPAC_ID)
        self.assertEqual(self.expansion.name(), 'Shadowbringers')

    def test_expansion_list(self) -> None:
        '''
        The client should be able to fetch a list of all expansions.
        '''
        expacs = self.client.get_all_expansions()

        self.assertIsInstance(expacs, list)
        self.assertGreater(len(expacs), 0)
        for expac in expacs:
            self.assertIsInstance(expac, FFLogsExpansion)

    def test_zones(self) -> None:
        '''
        The client should be able to fetch a list of all zones belonging to the expansion.
        '''
        zones = self.expansion.zones()

        self.assertIsInstance(zones, list)
        self.assertGreater(len(zones), 0)
        for zone in zones:
            self.assertIsInstance(zone, FFLogsZone)


if __name__ == '__main__':
    unittest.main()
