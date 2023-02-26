import os
import pickle
from copy import deepcopy
from time import time
from typing import Any, Dict

import oauthlib.oauth2 as oauth2
from gql import Client as GQLClient
from gql import gql
from gql.transport.requests import RequestsHTTPTransport
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from .characters.client_extensions import CharactersMixin
from .reports.client_extensions import ReportsMixin
from .world.client_extensions import WorldMixin


def ensure_token(func):
    '''
    Ensures the given function has a valid OAuth token
    '''
    def ensured(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except Exception:
            self.token = self.oauth_session.fetch_token(
                self.OAUTH_TOKEN_URL,
                auth=self.auth,
            )
            return func(*args, **kwargs)
    return ensured


class FFLogsClient(
    ReportsMixin,
    CharactersMixin,
    WorldMixin,
):
    '''
    A client capable of communicating with the FFLogs V2 GraphQL API.
    '''

    CLIENT_API_URL = 'https://www.fflogs.com/api/v2/client'
    OAUTH_TOKEN_URL = 'https://www.fflogs.com/oauth/token'
    CACHE_DIR = './querycache'

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        enable_caching: bool = True,
        cache_expiry: int = 86400,
        cache_override: str = '',
        ignore_cache_expiry: bool = False,
    ) -> None:
        '''
        Initialize the FFLogs API client.

        Args:
            client_id: Client application ID
            client_secret: Client application secret
            enable_caching: If enabled, the client will cache the result of queries
                            for up to a time specified by the cache_expiry argument
            cache_expiry: How long to keep query results in cache, in seconds. Default is 1 day.
            cache_override: If set, force the client to load cached queries from the given file path
            ignore_cache_expiry: If set to True, the client will load the most up-to-date cache,
                                 even if it has expired
        '''
        self.auth = HTTPBasicAuth(client_id, client_secret)
        self.oauth_session = OAuth2Session(client=oauth2.BackendApplicationClient(client_id))
        self.token = {}

        self._query_cache = {}
        self.cache_expiry = cache_expiry
        self.cache_queries = enable_caching
        self.ignore_cache_expiry = ignore_cache_expiry

        if enable_caching:
            if not os.path.exists(self.CACHE_DIR):
                os.makedirs(self.CACHE_DIR)

            cache_path = ''
            if cache_override:
                cache_path = cache_override
            else:
                # pluck the freshest pickled cache and use that
                cache_files = list(filter(
                    lambda f: f.endswith('.pkl') and f[:-4].replace('.', '').isdigit(),
                    os.listdir(self.CACHE_DIR)
                ))
                if len(cache_files):
                    max_expiry_cache = max(cache_files, key=lambda fn: float(fn[:-4]))
                    cache_path = os.path.join(self.CACHE_DIR, max_expiry_cache)

            if cache_path:
                with open(cache_path, 'rb') as f:
                    self._query_cache = pickle.load(f)

        self._transport = RequestsHTTPTransport(url=self.CLIENT_API_URL)
        self._gql_client = GQLClient(transport=self._transport, fetch_schema_from_transport=True)

    def close(self):
        self.oauth_session.close()
        self._transport.close()

    @ensure_token
    def q(self, query: str, ignore_cache: bool = False) -> Dict[str, Any]:
        '''
        Executes a GraphQL query against the FFLogs API

        Args:
            query: The GraphQL query to execute
            ignore_cache: Whether or not to ignore cached results, forcing a re-fetch of the data.
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
        Stores the cached queries in pickled format
        '''
        if not os.path.exists(self.CACHE_DIR):
            os.makedirs(self.CACHE_DIR)

        # annotate the cache file with the largest expiry time
        # that way cache files with a timestamp larger than the current time are fully expired
        max_expiry = max(self._query_cache.values(), key=lambda q: q[0])
        cache_file_path = os.path.join(self.CACHE_DIR, f'{max_expiry[0]}.pkl')
        with open(cache_file_path, 'wb+') as f:
            pickle.dump(self._query_cache, f)

        if not silent:
            print(f'Cache saved to {cache_file_path}')

    def extend_cache(self, extension_time: int) -> None:
        '''
        Extend the lifetime of cache entries

        Args:
            extension_time: How much time to add to the cache entry expiry time
        '''
        for query, entry in self._query_cache.items():
            self._query_cache[query] = (entry[0] + extension_time, entry[1])

    def clean_cache(self) -> None:
        '''
        Delete expired cache files
        '''
        cache_files = list(filter(
            lambda f: f.endswith('.pkl') and f[:-4].replace('.', '').isdigit(),
            os.listdir(self.CACHE_DIR)
        ))
        if len(cache_files):
            for file in cache_files:
                expiry = float(file[:-4])
                if time() >= expiry:
                    os.remove(os.path.join(self.CACHE_DIR, file))
