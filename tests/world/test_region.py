import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.world.region import (
    FFLogsRegion,
    FFLogsSubregion,
    FFLogsServer,
    FFLogsRegionServerPage,
    FFLogsRegionServerPaginationIterator,
)
from ..config import *

class RegionTest(unittest.TestCase):
    '''
    Test cases for FFLogs region information.
    '''

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        self.region = self.client.get_region(id=1)

    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_all_regions(self) -> None:
        '''
        The client should be able to fetch a list of all supported regions.
        '''
        regions = self.client.get_all_regions()
        for region in regions:
            self.assertIsInstance(region, FFLogsRegion)
            self.assertIsNotNone(region.name())

    def test_simple_fields(self) -> None:
        '''
        The client should be able to fetch simple fields about the region.
        '''
        self.assertEqual(self.region.name(), 'North America')
        self.assertEqual(self.region.compact_name(), 'NA')
        self.assertEqual(self.region.slug(), 'NA')

    def test_subregions(self) -> None:
        '''
        The client should be able to provide a list of subregions belonging to the region
        '''
        subregions = self.region.subregions()
        for sr in subregions:
            self.assertIsInstance(sr, FFLogsSubregion)
    
    def test_servers(self) -> None:
        '''
        The client should be able to provide a pagination of servers belonging to the region
        '''
        pages = self.region.servers()
        self.assertIsInstance(pages, FFLogsRegionServerPaginationIterator)

        page = pages.__next__()
        self.assertIsInstance(page, FFLogsRegionServerPage)

        server = page.__iter__().__next__()
        self.assertIsInstance(server, FFLogsServer)

if __name__ == '__main__':
    unittest.main()
