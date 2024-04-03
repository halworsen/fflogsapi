'''
The client implementation that allows communication with the FF Logs API.
'''

import os
import pickle
import tempfile
from copy import deepcopy
from functools import wraps
from time import time
from typing import Any
from warnings import warn

from gql import Client as GQLClient
from gql import gql
from gql.transport.requests import RequestsHTTPTransport
from oauthlib.oauth2 import BackendApplicationClient, WebApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from .characters.client_extensions import CharactersMixin
from .game.client_extensions import GameDataMixin
from .guilds.client_extensions import GuildsMixin
from .prograce.client_extensions import ProgressRaceMixin
from .reports.client_extensions import ReportsMixin
from .user.client_extensions import UserMixin
from .user_auth import UserModeAuthMixin
from .world.client_extensions import WorldMixin


def ensure_token(func):
    '''
    Ensures the given function has a valid OAuth token.
    '''
    @wraps(func)
    def ensured(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except Exception:
            if self.mode == 'user':
                # for user mode, the user must login through their browser
                # see user_auth.py
                self.user_auth()
            elif self.mode == 'client':
                self.token = self.oauth_session.fetch_token(
                    self.OAUTH_TOKEN_URL,
                    auth=self.auth,
                )
            return func(*args, **kwargs)
    return ensured


class FFLogsClient(
    UserModeAuthMixin,
    ReportsMixin,
    CharactersMixin,
    GuildsMixin,
    WorldMixin,
    UserMixin,
    GameDataMixin,
    ProgressRaceMixin,
):
    '''
    A client capable of communicating with the FF Logs V2 GraphQL API.

    Caching is enabled by default, but can be overriden with the enable_caching parameter when
    instantiating the client. A cache of executed queries will then be maintained by the client.
    To save the query cache for later reuse, you must manually call :func:`save_cache` on the
    client. It's also possible to extend the lifetime of all cache queries with
    :func:`extend_cache`, or to manually clean up old cache files with :func:`clean_cache`.

    Two modes of use are supported by the client - ``client`` and ``user`` mode.
    When in client mode, the API client can access the public API. To access private information
    such as private logs or hidden characters' information, you *must* use user mode.

    Args:
        client_id: Client application ID
        client_secret: Client application secret
        mode: Whether to use the client or user endpoint. Client mode gives public API access,
              while user mode allows access to private information. User mode requires login.
        enable_caching: If enabled, the client will cache the result of queries
                        for up to a time specified by the cache_expiry argument.
        cache_directory: The directory to read and save query cache files in.
        cache_expiry: How long to keep query results in cache, in seconds. Default is 1 day.
        cache_override: If set, force the client to load cached queries from the given file path
        ignore_cache_expiry: If set to True, the client will load the most up-to-date cache,
                             even if it has expired
        clean_cache: Automatically remove expired cache files from the cache directory

    Raises:
        ValueError if the provided client mode is invalid.
    '''

    API_URL = 'https://www.fflogs.com/api/v2'
    CLIENT_ENDPOINT = '/client'
    USER_ENDPOINT = '/user'

    OAUTH_TOKEN_URL = 'https://www.fflogs.com/oauth/token'

    Q_RATE_LIMIT = 'query{{rateLimitData{innerQuery}}}'

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        mode: str = 'client',
        enable_caching: bool = True,
        cache_directory: str = './fflogs-querycache',
        cache_expiry: int = 86400,
        cache_override: str = '',
        ignore_cache_expiry: bool = False,
        clean_cache: bool = True,
    ) -> None:
        self.auth = HTTPBasicAuth(client_id, client_secret)
        oauth_client = None
        if mode == 'client':
            oauth_client = BackendApplicationClient(client_id=client_id)
        elif mode == 'user':
            oauth_client = WebApplicationClient(client_id=client_id)
        else:
            raise ValueError(
                f'Invalid API client mode (must be either \'client\' or \'user\', got {mode})'
            )
        self.oauth_session = OAuth2Session(client=oauth_client)
        self.token = {}
        self.mode = mode

        self._query_cache = {}
        self.cache_expiry = cache_expiry
        self.cache_queries = enable_caching
        self.ignore_cache_expiry = ignore_cache_expiry

        # deprecation warning for cache_directory use
        if cache_directory != './fflogs-querycache':
            warn('Custom cache directories are deprecated in favor of system temp dirs.'
                 ' Consider removing usage of cache_directory when instantiating FFLogsClient.',
                 category=FutureWarning)
        else:
            # future behavior
            self.cache_dir = os.path.join(tempfile.gettempdir(), 'fflogsapi')

        if enable_caching:
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)

            cache_path = ''
            if cache_override:
                cache_path = cache_override
            else:
                # pluck the freshest pickled cache and use that
                cache_files = list(filter(
                    lambda f: f.endswith('.pkl') and f[:-4].replace('.', '').isdigit(),
                    os.listdir(self.cache_dir)
                ))
                if len(cache_files):
                    max_expiry_cache = max(cache_files, key=lambda fn: float(fn[:-4]))
                    cache_path = os.path.join(self.cache_dir, max_expiry_cache)

            if cache_path:
                with open(cache_path, 'rb') as f:
                    self._query_cache = pickle.load(f)

        if clean_cache:
            self.clean_cache()

        endpoint = self.CLIENT_ENDPOINT if mode == 'client' else self.USER_ENDPOINT
        self._transport = RequestsHTTPTransport(url=self.API_URL + endpoint)
        self._gql_client = GQLClient(transport=self._transport, fetch_schema_from_transport=True)

    def close(self) -> None:
        '''
        Close the OAuth session with the FF Logs API
        '''
        self.oauth_session.close()
        self._transport.close()

    @ensure_token
    def q(self, query: str, ignore_cache: bool = False) -> dict[str, Any]:
        '''
        Executes a raw GraphQL query against the FFLogs API.

        Generally, you should not use this unless you need to execute a query that is not properly
        supported by the client. You can also use this function to query for more information in
        batch than the client normally would.

        The result of the query is stored in cache by default, and will be returned in place of a
        real query result if the same query is repeated. If you need up-to-date query results,
        use `ignore_cache` to force the client to query the actual API for the information.
        Note that the result is still cached if the client has caching enabled, so any repeat of
        the same query that does not use `ignore_cache` will always return the last result of
        actually executing the query.

        Args:
            query: The GraphQL query to execute.
            ignore_cache: Whether or not to ignore cached results, forcing a query to be executed
                          against the API.

        Returns:
            The result of the query as a dictionary.
        '''
        if self.cache_queries and not ignore_cache and query in self._query_cache:
            cached_result = self._query_cache[query]
            # expired entry
            if not self.ignore_cache_expiry and time() >= cached_result[0]:
                self._query_cache.pop(query)
            else:
                return deepcopy(cached_result[1])

        access_token = self.token['access_token']
        self._transport.headers = {'Authorization': f'Bearer {access_token}'}
        gql_q = gql(query)
        result = self._gql_client.execute(gql_q)

        if self.cache_queries:
            self._query_cache[query] = (time() + self.cache_expiry, result)

        return deepcopy(result)

    def save_cache(self, silent: bool = True) -> None:
        '''
        Stores all cached queries in pickled format.

        The query cache file is stored in the cache directory. The file name is the the
        unix timestamp of the query with the largest expiry time. This means that there is
        no guarantee that *all* results in the cache are usable, but there is at least *some*
        useful data in the cache.

        Args:
            silent: If False, print the path of the cache file.
        '''
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        # annotate the cache file with the largest expiry time
        # that way cache files with a timestamp larger than the current time are fully expired
        max_expiry = max(self._query_cache.values(), key=lambda q: q[0])
        cache_file_path = os.path.join(self.cache_dir, f'{max_expiry[0]}.pkl')
        with open(cache_file_path, 'wb+') as f:
            pickle.dump(self._query_cache, f)

        if not silent:
            print(f'Cache saved to {cache_file_path}')

    def extend_cache(self, extension_time: int) -> None:
        '''
        Extend the lifetime of all cache entries.

        Args:
            extension_time: How much time to add to the cache entries' expiry time, in seconds.
        '''
        for query, entry in self._query_cache.items():
            self._query_cache[query] = (entry[0] + extension_time, entry[1])

    def clean_cache(self) -> None:
        '''
        Delete expired cache files.

        This goes through the cache file directory, deleting all pickled files with a timestamp less
        than the current unix timestamp. Such cache files are guaranteed not to contain useful data
        anymore.
        '''
        cache_files = list(filter(
            lambda f: f.endswith('.pkl') and f[:-4].replace('.', '').isdigit(),
            os.listdir(self.cache_dir)
        ))
        if len(cache_files):
            for file in cache_files:
                expiry = float(file[:-4])
                if time() >= expiry:
                    os.remove(os.path.join(self.cache_dir, file))

    def rate_limit_allowance(self) -> int:
        '''
        Fetches the amount of points the API client is allowed to spend each hour.

        Returns:
            The total point allowance of the API client.
        '''
        return self.q(self.Q_RATE_LIMIT.format(
            innerQuery='limitPerHour'
        ))['rateLimitData']['limitPerHour']

    def rate_limit_reset_time(self) -> int:
        '''
        Fetches the amount of seconds remaining until the point allowance resets for
        the current API client.

        Returns:
            Seconds left until points reset.
        '''
        return self.q(self.Q_RATE_LIMIT.format(
            innerQuery='pointsResetIn'
        ))['rateLimitData']['pointsResetIn']

    def rate_limit_spent(self) -> float:
        '''
        Fetches the amount of points that have been spent by the API client the past hour.

        Returns:
            The amount of points spent.
        '''
        return self.q(self.Q_RATE_LIMIT.format(
            innerQuery='pointsSpentThisHour'
        ))['rateLimitData']['pointsSpentThisHour']
