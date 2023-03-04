import unittest

from fflogsapi.characters.character import FFLogsCharacter
from fflogsapi.client import FFLogsClient
from fflogsapi.world.pages import FFLogsServerCharacterPage, FFLogsServerCharacterPaginationIterator
from fflogsapi.world.region import FFLogsRegion, FFLogsSubregion

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class ServerTest(unittest.TestCase):
    '''
    Test cases for FFLogs server information.
    '''

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.server = cls.client.get_server(id=1)
        cls.server_by_filters = cls.client.get_server(filters={
            'region': 'NA',
            'slug': 'Adamantoise',
        })

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_server_by_filters(self) -> None:
        '''
        The client should be able to get a server by both ID and region+slug.
        '''
        self.assertEqual(self.server.id(), self.server_by_filters.id())

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
