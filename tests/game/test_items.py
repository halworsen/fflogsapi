import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.game.dataclasses import FFItem
from fflogsapi.game.pages import FFLogsItemPage

from ..config import CLIENT_ID, CLIENT_SECRET


class GameItemTest(unittest.TestCase):
    '''
    Test cases for the game items.
    '''

    ITEM_ID = 2134

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
        cls.item = cls.client.item(id=cls.ITEM_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_item(self) -> None:
        '''
        The client should be able to get information about a game item.
        '''
        self.assertEqual(self.item.id, self.ITEM_ID)
        self.assertEqual(self.item.name, 'Aetherial Ivory Staff')
        self.assertEqual(self.item.icon, '033000-033017.png')

    def test_item_pagination(self) -> None:
        '''
        The client should be able to get a pagination of all game items.
        '''
        items = self.client.items()
        first_page = items.__next__()
        self.assertIsInstance(first_page, FFLogsItemPage)
        item: FFItem = filter(lambda i: i.id == 1, first_page.__iter__()).__next__()
        self.assertIsInstance(item, FFItem)

        self.assertEqual(item.id, 1)
        self.assertEqual(item.name, 'Gil')
        self.assertEqual(item.icon, '065000-065002.png')


if __name__ == '__main__':
    unittest.main()
