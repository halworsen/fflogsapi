import os
import tempfile
import unittest
from time import sleep, time

from fflogsapi.client import FFLogsClient

from ..config import CLIENT_ID, CLIENT_SECRET


class CacheTest(unittest.TestCase):
    '''
    Test cases for the client's query caching functionality.

    WARNING: Running these tests will delete all existing query caches!
    '''
    CACHE_EXPIRY = 2  # seconds

    @classmethod
    def setUpClass(cls) -> None:
        # The cache directory must be empty before starting these tests (if it exists)
        cache_dir = os.path.join(tempfile.gettempdir(), 'fflogsapi')
        if os.path.exists(cache_dir):
            for fn in os.listdir(cache_dir):
                os.remove(os.path.join(cache_dir, fn))
            os.rmdir(cache_dir)

        cls.client = FFLogsClient(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            cache_expiry=cls.CACHE_EXPIRY
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()

    def setUp(self) -> None:
        # Query for some expansion information to get a query in the cache
        expac = self.client.get_expansion(id=1)
        expac.name()

    def test_caching(self) -> None:
        '''
        The client should not break when using data from cache.
        '''
        # same code is already run during setup
        expac = self.client.get_expansion(id=1)
        expac.name()

    def test_cache_saving(self) -> None:
        '''
        The client should be able to save a file containing cached query results
        '''
        self.client.save_cache(silent=False)
        self.assertTrue(os.path.exists(self.client.cache_dir))
        cache_expiry = list(map(lambda f: float(f[:-4]), os.listdir(self.client.cache_dir)))[0]
        self.assertAlmostEqual(time() + self.CACHE_EXPIRY, cache_expiry, places=1)

    def test_extend_cache(self) -> None:
        '''
        The client should be able to extend the lifetime of the cache.
        '''
        self.client.extend_cache(2)
        self.client.save_cache()

        expiries = list(map(lambda f: float(f[:-4]), os.listdir(self.client.cache_dir)))
        ok = False
        for expiry in expiries:
            if round(time() + self.CACHE_EXPIRY + 2, 1) == round(expiry, 1):
                ok = True
                break
        self.assertTrue(ok, msg='No caches expire after the correct timestamp')

    def test_clean_cache(self) -> None:
        '''
        The client should be able to clean up expired caches.
        '''
        self.client.save_cache()

        expiries = list(map(lambda f: float(f[:-4]), os.listdir(self.client.cache_dir)))
        # is soonest even a word?
        soonest_expire = min(expiries)

        # we shouldn't have to wait long
        self.assertLessEqual(soonest_expire - time(), self.CACHE_EXPIRY)

        # wait until the cache is guaranteed to have expired (should be at most a few seconds)
        sleep(soonest_expire - time())

        self.assertGreaterEqual(time(), soonest_expire)

        self.client.clean_cache()
        expiries = list(map(lambda f: float(f[:-4]), os.listdir(self.client.cache_dir)))

        self.assertNotIn(soonest_expire, expiries)


if __name__ == '__main__':
    unittest.main()
