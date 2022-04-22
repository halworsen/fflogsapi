from gql import gql
from gql import Client as GQLClient
from gql.transport.requests import RequestsHTTPTransport
import oauthlib.oauth2 as oauth2
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth

from .queries import *
from .data import Report, Fight

def ensure_token(func):
    '''
    Ensures the given function has a valid OAuth token
    '''
    def ensured(*args, **kwargs):
        self = args[0]
        try:
            return func(*args, **kwargs)
        except:
            self.token = self.oauth_session.fetch_token(
                self.OAUTH_TOKEN_URL,
                auth=self.auth,
            )
            return func(*args, **kwargs)
    return ensured


class FFLogsClient:

    CLIENT_API_URL = 'https://www.fflogs.com/api/v2/client'
    OAUTH_TOKEN_URL = 'https://www.fflogs.com/oauth/token'

    def __init__(self, client_id, client_secret):
        '''
        Initialize the FFLogs API client

        Args:
            client_id: Client application ID
            client_secret: Client application secret
        '''
        self.auth = HTTPBasicAuth(client_id, client_secret)
        self.oauth_session = OAuth2Session(client=oauth2.BackendApplicationClient(client_id))
        self.token = {}

        self.transport = RequestsHTTPTransport(url=self.CLIENT_API_URL)
        self.gql_client = GQLClient(transport=self.transport, fetch_schema_from_transport=True)

    @ensure_token
    def q(self, query):
        '''
        Executes a GraphQL query against the FFLogs API

        Args:
            query: The GraphQL query to execute
        '''
        access_token = self.token['access_token']
        self.transport.headers = {'Authorization': f'Bearer {access_token}'}
        gql_q = gql(query)
        result = self.gql_client.execute(gql_q)
        return result
    
    def get_pages(self, gid, inner_query):
        '''
        Retrieves the desired information from all report pages
        '''
        more_pages = True
        page = 1
        report_data = []
        while more_pages:
            result = self.q(Q_PAGINATED_REPORTS.format(
                guildID=gid,
                page=page,
                innerQuery=inner_query,
            ))
            report_data += result['reportData']['reports']['data']
            more_pages = result['reportData']['reports']['has_more_pages']
            page += 1

        return report_data
    
    def get_all_reports(self, gid):
        '''
        Retrieves all public reports by a given user, including fights
        '''
        reports = self.get_pages(gid, Q_INNER_REPORTS)

        all_reports = {}
        for report_data in reports:
            report = Report(
                code=report_data['code'],
                title=report_data['title'],
                owner=report_data['owner'],
                start=report_data['startTime'],
                end=report_data['endTime'],
            )
            all_reports[report.code] = report

        all_fights = {}
        # due to complexity limits we need to retrieve all the information with 2 queries
        fight_meta = self.get_pages(gid, Q_INNER_FIGHTS_META)
        fight_detail = self.get_pages(gid, Q_INNER_FIGHTS_DETAIL)
        for report_data in fight_meta:
            all_fights[report_data['code']] = {}
            for fight_data in report_data['fights']:
                fight = Fight(
                    id=fight_data['id'],
                    difficulty=fight_data['difficulty'],
                    start=fight_data['startTime'],
                    end=fight_data['endTime'],
                )
                all_fights[report_data['code']][fight.id] = fight

        for report_data in fight_detail:
            fight_report = all_fights[report_data['code']]
            for fight_data in report_data['fights']:
                fight = fight_report[fight_data['id']]
                fight.name = fight_data['name']
                fight.kill = fight_data['kill']
                fight.fightPercentage = fight_data['fightPercentage']

                report = all_reports[report_data['code']]
                report.add_fight(fight)

        return list(all_reports.values())
