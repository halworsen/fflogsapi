import unittest

from fflogsapi.client import FFLogsClient

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class CharacterTest(unittest.TestCase):
    '''
    Test cases for FF Logs characters.

    This test is severely limited by the fact that it's a large hassle to perform
    user mode tests as they require an actual FF Logs login. Technically, we could use selenium
    to automate this, but creating a dedicated FF Logs user for these tests could technically
    be seen as a circumvention of the API rate limiting, which is against the API ToS.

    We can test for the error behavior of the client when attempting to access parts of the API that
    require user privilege, however.
    '''

    USER_ID = 34534

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(
            CLIENT_ID,
            CLIENT_SECRET,
            mode='client',
            cache_expiry=CACHE_EXPIRY
        )
        cls.user = cls.client.get_user(id=cls.USER_ID)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_current_user(self) -> None:
        '''
        The client should raise an error when attempting to fetch the current user in client mode.
        '''
        with self.assertRaises(PermissionError):
            self.client.get_current_user()

    def test_user(self) -> None:
        '''
        The client should be able to fetch any user's username.
        '''
        self.assertEqual(self.user.id, self.USER_ID)
        self.assertEqual(self.user.name(), 'Kazzio')

    def test_user_characters(self) -> None:
        '''
        The client should raise an error when attempting to fetch a character while in client mode.
        '''
        with self.assertRaises(Exception):
            self.user.characters()

    def test_user_guilds(self) -> None:
        '''
        The client should be able to get a list of the guilds that a character belongs to.
        '''
        with self.assertRaises(Exception):
            self.user.guilds()


if __name__ == '__main__':
    unittest.main()
