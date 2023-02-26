import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.world.region import (
    FFLogsRegion,
    FFLogsServer,
    FFLogsSubregionServerPage,
    FFLogsSubregionServerPaginationIterator,
)
from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET

class SubregionTest(unittest.TestCase):
    '''
    Test cases for FFLogs subregion information.
    '''

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        self.subregion = self.client.get_subregion(id=1)

    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_name(self) -> None:
        '''
        The client should be able to fetch the name of the subregion.
        '''
        self.assertEqual(self.subregion.name(), 'Aether')

    def test_region(self) -> None:
        '''
        The client should be able to get the region to which a subregion belongs to.
        '''
        region = self.subregion.region()
        self.assertIsInstance(region, FFLogsRegion)
        self.assertEqual(region.slug(), 'NA')

    def test_servers(self) -> None:
        '''
        The client should be able to provide a pagination of servers belonging to the subregion
        '''
        pages = self.subregion.servers()
        self.assertIsInstance(pages, FFLogsSubregionServerPaginationIterator)

        page = pages.__next__()
        self.assertIsInstance(page, FFLogsSubregionServerPage)

        server = page.__iter__().__next__()
        self.assertIsInstance(server, FFLogsServer)

if __name__ == '__main__':
    unittest.main()