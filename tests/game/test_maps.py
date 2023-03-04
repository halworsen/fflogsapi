import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.game.dataclasses import FFMap
from fflogsapi.game.pages import FFLogsMapPage

from ..config import CLIENT_ID, CLIENT_SECRET


class GameMapTest(unittest.TestCase):
    '''
    Test cases for the game maps.
    '''

    MAP_ID = 3

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
        cls.map = cls.client.map(id=cls.MAP_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_map(self) -> None:
        '''
        The client should be able to get information about a game map.
        '''
        self.assertEqual(self.map.id, self.MAP_ID)
        self.assertEqual(self.map.name, 'Old Gridania')
        self.assertEqual(self.map.filename, 'm-f1t2-f1t2.00.jpg')
        self.assertEqual(self.map.offset_x, 0)
        self.assertEqual(self.map.offset_y, 0)
        self.assertEqual(self.map.size_factor, 200)

    def test_map_pagination(self) -> None:
        '''
        The client should be able to get a pagination of all game maps.
        '''
        maps = self.client.maps()
        first_page = maps.__next__()
        self.assertIsInstance(first_page, FFLogsMapPage)
        map: FFMap = filter(lambda m: m.id == 1, first_page.__iter__()).__next__()
        self.assertIsInstance(map, FFMap)

        self.assertEqual(map.id, 1)
        self.assertEqual(map.name, 'Eorzea')
        self.assertEqual(map.filename, 'm-default-default.00.jpg')
        self.assertEqual(map.offset_x, 0)
        self.assertEqual(map.offset_y, 0)
        self.assertEqual(map.size_factor, 100)


if __name__ == '__main__':
    unittest.main()
