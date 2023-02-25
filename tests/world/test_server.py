import unittest
from fflogsapi.characters.character import FFLogsCharacter

from fflogsapi.client import FFLogsClient
from fflogsapi.world.pages import FFLogsServerCharacterPage, FFLogsServerCharacterPaginationIterator
from fflogsapi.world.region import FFLogsRegion, FFLogsSubregion
from ..config import *

class ServerTest(unittest.TestCase):
    '''
    Test cases for FFLogs server information.
    '''

    def setUp(self) -> None:
        self.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        self.server = self.client.get_server(id=1)

    def tearDown(self) -> None:
        self.client.close()
        self.client.save_cache()

    def test_simple_fields(self) -> None:
        '''
        The client should be able to fetch simple fields about the server.
        '''
        self.assertEqual(self.server.name(), 'Adamantoise')
        self.assertEqual(self.server.normalized_name(), 'adamantoise')
        self.assertEqual(self.server.slug(), 'adamantoise')

    def test_region(self) -> None:
        '''
        The client should be able to get the region to which a server belongs to.
        '''
        region = self.server.region()
        self.assertIsInstance(region, FFLogsRegion)
        self.assertEqual(region.slug(), 'NA')

    def test_subregion(self) -> None:
        '''
        The client should be able to get the subregion to which a server belongs to.
        '''
        subregion = self.server.subregion()
        self.assertIsInstance(subregion, FFLogsSubregion)
        self.assertEqual(subregion.name(), 'Aether')

    def test_characters(self) -> None:
        '''
        The client should be able to provide a pagination of characters belonging to the server.
        '''
        pages = self.server.characters()
        self.assertIsInstance(pages, FFLogsServerCharacterPaginationIterator)

        page = pages.__next__()
        self.assertIsInstance(page, FFLogsServerCharacterPage)

        character = page.__iter__().__next__()
        self.assertIsInstance(character, FFLogsCharacter)
        self.assertIsNotNone(character.name())

if __name__ == '__main__':
    unittest.main()