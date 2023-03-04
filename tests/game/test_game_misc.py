import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.game.dataclasses import FFJob

from ..config import CLIENT_ID, CLIENT_SECRET


class GameItemTest(unittest.TestCase):
    '''
    Test cases for miscellaneous game data features.
    '''

    ITEM_ID = 2134
    MAP_ID = 3

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
        cls.item = cls.client.item(id=cls.ITEM_ID)
        cls.map = cls.client.map(id=cls.MAP_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_icon_url(self) -> None:
        '''
        The client should be able to get full icon URLs.
        '''
        self.assertEqual(
            self.client.icon_url(self.item.icon),
            'https://assets.rpglogs.com/img/ff/abilities/033000-033017.png',
        )

        self.assertEqual(
            self.client.icon_url(self.map.filename),
            'https://assets.rpglogs.com/img/ff/maps/m-f1t2-f1t2.00.jpg',
        )

    def test_jobs(self) -> None:
        '''
        The client should be able to get a list of all jobs.
        '''
        jobs = self.client.jobs()
        self.assertIsInstance(jobs, list)
        self.assertGreater(len(jobs), 0)
        self.assertIsInstance(jobs[0], FFJob)

        rdm = filter(lambda j: j.name == 'Red Mage', jobs).__next__()
        self.assertEqual(rdm.id, 14)
        self.assertEqual(rdm.name, 'Red Mage')
        self.assertEqual(rdm.slug, 'RedMage')

        all_jobs = [
            'Astrologian', 'Bard', 'Black Mage', 'Dark Knight', 'Dragoon',
            'Machinist', 'Monk', 'Ninja', 'Paladin', 'Scholar',
            'Summoner', 'Warrior', 'White Mage', 'Red Mage', 'Samurai',
            'Dancer', 'Gunbreaker', 'Reaper', 'Sage',
        ]
        job_names = [job.name for job in jobs]
        self.assertListEqual(sorted(job_names), sorted(all_jobs))

    def test_grand_companies(self) -> None:
        '''
        The client should be able to get a list of all grand companies.
        '''
        gcs = self.client.grand_companies()
        all_gcs = ['Order of the Twin Adder', 'The Immortal Flames', 'The Maelstrom']
        gc_names = [gc.name for gc in gcs]
        self.assertListEqual(sorted(all_gcs), sorted(gc_names))


if __name__ == '__main__':
    unittest.main()
