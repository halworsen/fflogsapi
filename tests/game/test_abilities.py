import unittest

from fflogsapi.client import FFLogsClient
from fflogsapi.game.dataclasses import FFAbility
from fflogsapi.game.pages import FFLogsAbilityPage

from ..config import CLIENT_ID, CLIENT_SECRET


class GameAbilityTest(unittest.TestCase):
    '''
    Test cases for the game abilities.
    '''

    ABILITY_ID = 3615

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET)
        cls.ability = cls.client.ability(id=cls.ABILITY_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_unknown_ability(self) -> None:
        '''
        The 'unknown ability' should be supported.
        '''
        unkn = self.client.ability(id=0)
        self.assertEqual(unkn.name, 'Unknown Ability')

    def test_ability(self) -> None:
        '''
        The client should be able to get information about a game ability.
        '''
        self.assertEqual(self.ability.id, self.ABILITY_ID)
        self.assertEqual(self.ability.name, 'Gravity')
        self.assertEqual(
            self.ability.description,
            'Deals unaspected damage with a potency of 120 to target and all enemies nearby it.'
        )
        self.assertEqual(self.ability.icon, '003000-003123.png')

    def test_ability_pagination(self) -> None:
        '''
        The client should be able to get a pagination of all game abilities.
        '''
        abilities = self.client.abilities()
        first_page = abilities.__next__()
        self.assertIsInstance(first_page, FFLogsAbilityPage)
        ability: FFAbility = filter(lambda a: a.id == 1, first_page.__iter__()).__next__()
        self.assertIsInstance(ability, FFAbility)

        self.assertEqual(ability.id, 1)
        self.assertEqual(ability.name, 'Key Item')
        self.assertEqual(ability.description, '')
        self.assertEqual(ability.icon, '000000-000405.png')


if __name__ == '__main__':
    unittest.main()
