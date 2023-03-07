import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.world.pages import FFLogsSubregionServerPage, FFLogsSubregionServerPaginationIterator
from fflogsapi.world.region import FFLogsRegion
from fflogsapi.world.server import FFLogsServer

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class SubregionTest(unittest.TestCase):
    '''
    Test cases for FF Logs subregion information.
    '''

    SUBREGION_ID = 1

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.subregion = cls.client.get_subregion(id=cls.SUBREGION_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_fields(self) -> None:
        '''
        The client should be able to fetch the id and name of the subregion.
        '''
        self.assertEqual(self.subregion.id(), self.SUBREGION_ID)
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
