from typing import TYPE_CHECKING, List, Optional
from fflogsapi.reports.fight import FFLogsFight

from fflogsapi.iterators.report_iterator import FFLogsReportIterator
from fflogsapi.data.dataclasses import FFLogsAbility, FFLogsActor
import fflogsapi.queries as qs

if TYPE_CHECKING:
    from fflogsapi.client import FFLogsClient


def fetch_data(key):
    '''
    Decorator that queries and stores the given key
    '''
    def decorator(func):
        def ensured(*args, **kwargs):
            self = args[0]
            if key not in self._data:
                result = self._query_data(key)
                self._data[key] = result['reportData']['report'][key]
            return func(*args, **kwargs)
        return ensured
    return decorator

def fetch_master_data(func):
    '''
    Decorator that queries for master data if needed before the function
    '''
    def ensured(*args, **kwargs):
        self = args[0]
        if 'masterData' not in self._data:
            self._get_master_data()
        return func(*args, **kwargs)
    return ensured


class FFLogsReport:
    '''
    Representation of a report on FFLogs.
    '''

    MASTER_DATA_QUERY = """
        masterData {
            logVersion
            actors {
                gameID
                id
                name
                server
                petOwner
                subType
                type
            }
            abilities {
                gameID
                name
                type
            }
        }
    """

    def __init__(self, code: str, client: 'FFLogsClient' = None) -> None:
        self.code = code
        self._fights = {}
        self._data = {}
        self._client = client

    def __iter__(self) -> FFLogsReportIterator:
        return FFLogsReportIterator(report=self, client=self._client)
    
    def fights(self) -> List[FFLogsFight]:
        return list(self.__iter__())
    
    def _query_data(self, query: str, ignore_cache: bool = False) -> None:
        '''
        Query for a specific piece of information from a report.
        '''
        result = self._client.q(qs.Q_REPORT_DATA.format(
            reportCode=self.code,
            innerQuery=query
        ), ignore_cache=ignore_cache)

        return result

    def _get_master_data(self) -> None:
        '''
        Fetches and stores report master data
        '''
        result = self._query_data(self.MASTER_DATA_QUERY)
        master_data = result['reportData']['report']['masterData']
        self._data['masterData'] = {
            'logVersion': master_data['logVersion'],
            'actors': [],
            'abilities': [],
        }

        for actor_data in master_data['actors']:
            actor = FFLogsActor(
                id=actor_data['id'],
                name=actor_data['name'],
                type=actor_data['type'],
                sub_type=actor_data['subType'],
                server=actor_data['server'],
                game_id=actor_data['gameID'],
                pet_owner=actor_data['petOwner'],
            )
            self._data['masterData']['actors'].append(actor)
        
        for ability_data in master_data['abilities']:
            ability = FFLogsAbility(
                game_id=ability_data['gameID'],
                name=ability_data['name'],
                type=ability_data['type'],
            )
            self._data['masterData']['abilities'].append(ability)

    def fetch_batch(self) -> None:
        '''
        Attempt to fetch and store large amounts of fights in a single query
        '''
        fight_query = ', '.join(FFLogsFight.batch_fields)
        query = f'fights {{ {fight_query} }}'
        result = self._query_data(query)
        data = result['reportData']['report']['fights']
        for fight_data in data:
            fight = self._fights.get(
                fight_data['id'],
                FFLogsFight(report=self, fight_id=fight_data['id'], client=self._client),
            )

            for field in FFLogsFight.batch_fields:
                fight._data[field] = fight_data[field]
            
            self._fights[fight_data['id']] = fight

    @fetch_master_data
    def actors(self) -> List[FFLogsActor]:
        '''
        Returns:
            A list of all actors in the report
        '''
        return self._data['masterData']['actors']
    
    @fetch_master_data
    def abilities(self) -> List[FFLogsAbility]:
        '''
        Returns:
            A list of all abilities in the report
        '''
        return self._data['masterData']['abilities']

    @fetch_master_data
    def log_version(self) -> int:
        '''
        Returns:
            The version of the client parser used to parse and upload the log file
        '''
        return self._data['masterData']['logVersion']

    @fetch_data('title')
    def title(self) -> str:
        return self._data['title']

    @fetch_data('owner')
    def owner(self) -> str:
        return self._data['owner']

    @fetch_data('guild')
    def end_time(self) -> float:
        return self._data['guild']

    @fetch_data('guildTag')
    def guild_tag(self) -> float:
        return self._data['guildTag']

    @fetch_data('zone')
    def zone(self) -> Optional[str]:
        return self._data['zone']

    @fetch_data('startTime')
    def start_time(self) -> float:
        return self._data['startTime']

    @fetch_data('endTime')
    def end_time(self) -> float:
        return self._data['endTime']
    
    @fetch_data('segments')
    def segments(self) -> int:
        return self._data['segments']
    
    def duration(self) -> float:
        '''
        Returns:
            The total duration of the report
        '''
        return self.end_time() - self.start_time()
    
    def fight_count(self) -> int:
        '''
        Returns:
            The total amount of fights in the report
        '''
        result = self._query_data('fights { id }')
        return len(result['reportData']['report']['fights'])

    def fight(self, id: int = -1) -> FFLogsFight:
        '''
        Args:
            id: The ID of the fight to retrieve. Default: last fight
        Returns:
            An FFLogsFight object or None if the fight is not in the report
        '''
        if id == -1:
            id = self.fight_count()

        if id < 1 or id > self.fight_count():
            return None

        if id not in self._fights:
            fight = FFLogsFight(
                report=self,
                fight_id=id,
                client=self._client,
            )
            self._fights[id] = fight

        return self._fights[id]