import unittest

from fflogsapi.world.dataclasses import FFLogsPartition

from fflogsapi.client import FFLogsClient
from fflogsapi.constants import FIGHT_DIFFICULTY_RAID, FIGHT_DIFFICULTY_SAVAGE
from fflogsapi.world.expansion import FFLogsExpansion
from fflogsapi.world.zone import FFLogsZone

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class ZoneTest(unittest.TestCase):
    '''
    Test cases for FF Logs zone information.
    '''

    ZONE_ID = 49

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)
        cls.zone = cls.client.get_zone(id=cls.ZONE_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_fields(self) -> None:
        '''
        The client should be able to fetch simple fields from the zone
        '''
        self.assertEqual(self.zone.id(), self.ZONE_ID)
        self.assertEqual(self.zone.name(), 'Abyssos')
        self.assertIsInstance(self.zone.frozen(), bool)

    def test_zone_list(self) -> None:
        '''
        The client should be able to retrieve a list of all supported zones in an expansion.
        '''
        zones = self.client.get_all_zones(expansion_id=1)
        first_zone = zones[0]
        self.assertIsInstance(first_zone, FFLogsZone)
        self.assertEqual(len(zones), 10)
        self.assertEqual(first_zone.id(), 13)

    def test_brackets(self) -> None:
        '''
        The client should be able to fetch bracket information from a zone.
        '''
        brackets = self.zone.brackets()
        self.assertEqual(brackets['min'], 6)

    def test_difficulties(self) -> None:
        '''
        The client should be able to fetch information about difficulties supported by the zone.
        '''
        difficulties = self.zone.difficulties()
        self.assertEqual(len(difficulties), 2)
        retrieved_difficulties = [d['id'] for d in difficulties]

        self.assertSetEqual(
            set(retrieved_difficulties),
            set((FIGHT_DIFFICULTY_RAID, FIGHT_DIFFICULTY_SAVAGE))
        )

    def test_encounter(self) -> None:
        '''
        The client should be able to get the encounters taking place in a zone.
        '''
        euphrosyne = self.client.get_zone(id=52)
        encounters = euphrosyne.encounters()
        retrieved_encounters = [e.name() for e in encounters]

        self.assertSetEqual(
            set(retrieved_encounters),
            set(('Nophica', 'Althyk and Nymeia', 'Halone', 'Menphina')),
        )

    def test_expansion(self) -> None:
        '''
        The client should be able to get the expansion to which a zone belongs.
        '''
        expac = self.zone.expansion()
        self.assertIsInstance(expac, FFLogsExpansion)
        self.assertEqual(expac.name(), 'Endwalker')

    def test_partitions(self) -> None:
        '''
        The client should be able to get information about partitions supported by a zone.
        '''
        partitions = self.zone.partitions(use_dataclass=True)
        self.assertIsNotNone(partitions)
        self.assertIsInstance(partitions[0], FFLogsPartition)
        self.assertIsInstance(partitions[0].id, int)
        self.assertIsInstance(partitions[0].name, str)


if __name__ == '__main__':
    unittest.main()
