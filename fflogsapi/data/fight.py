from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple
import fflogsapi.queries as qs

if TYPE_CHECKING:
    from fflogsapi.client import FFLogsClient
    from fflogsapi.data.report import FFLogsReport


def fetch_data(key):
    '''
    Decorator that queries and stores the given key
    '''
    def decorator(func):
        def ensured(*args, **kwargs):
            self = args[0]
            if key not in self._data:
                result = self._query_data(key)
                self._data[key] = result['reportData']['report']['fights'][0][key]
            return func(*args, **kwargs)
        return ensured
    return decorator


class FFLogsFight:
    '''
    Representation of a single fight on FFLogs.
    '''

    batch_fields = [
        "id", "name", "encounterID", "startTime", "endTime",
        "kill", "difficulty", "fightPercentage", "bossPercentage",
        "size", "standardComposition", "hasEcho"
    ]

    def __init__(self, report: 'FFLogsReport', fight_id: int, client: 'FFLogsClient') -> None:
        self.report = report
        self.fight_id = fight_id
        self._client = client
        self._data = {}

    def _query_data(self, query: str, ignore_cache: bool = False) -> Dict[Any, Any]:
        '''
        Query for a specific piece of information from a fight
        '''
        result = self._client.q(qs.Q_FIGHTDATA.format(
            reportCode=self.report.code,
            fightID=self.fight_id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def fetch_batch(self) -> None:
        '''
        Attempt to fetch and store large amounts of fight information in a single query
        '''
        result = self._query_data(', '.join(self.batch_fields))
        data = result['reportData']['report']['fights'][0]
        for field in self.batch_fields:
            self._data[field] = data[field]

    @fetch_data('name')
    def name(self) -> str:
        '''
        Returns:
            The name of the fight
        '''
        return self._data['name']

    @fetch_data('size')
    def size(self) -> int:
        '''
        Returns:
            The amount of players participating in the fight
        '''
        return self._data['size']

    @fetch_data('kill')
    def is_kill(self) -> bool:
        '''
        Returns:
            Whether or not the fight resulted in a kill
        '''
        return self._data['kill']

    @fetch_data('hasEcho')
    def has_echo(self) -> bool:
        '''
        Returns:
            Whether or not Echo was enabled for this fight
        '''
        return self._data['hasEcho']

    @fetch_data('standardComposition')
    def standard_comp(self) -> bool:
        '''
        Returns:
            Whether or not this fight had a standard composition.
            A standard composition is two tanks, two healers and four DPS.
        '''
        return self._data['standardComposition']

    @fetch_data('bossPercentage')
    def get_percentage(self) -> float:
        '''
        Returns:
            The minimum percentage of HP that was reached for the last boss in the fight
        '''
        return self._data['bossPercentage']

    @fetch_data('fightPercentage')
    def get_fight_percentage(self) -> float:
        '''
        Returns:
            The minimum percentage of the entire fight that was reached
        '''
        return self._data['fightPercentage']

    @fetch_data('difficulty')
    def get_difficulty(self) -> Optional[int]:
        '''
        Returns:
            The difficulty of the fight. Usually not very descriptive,
            as difficulty level 100 covers a wide variety of content.
        '''
        return self._data['difficulty']

    @fetch_data('encounterID')
    def get_encounter_id(self) -> int:
        '''
        Returns:
            The encounter ID of the fight
        '''
        return self._data['encounter_id']

    @fetch_data('startTime')
    def get_start_time(self) -> float:
        '''
        Returns:
            Start time of the fight relative to the start time of the report
        '''
        return self._data['startTime']

    @fetch_data('endTime')
    def get_end_time(self) -> float:
        '''
        Returns:
            End time of the fight relative to the start time of the report
        '''
        return self._data['endTime']

    def duration(self) -> float:
        '''
        Returns:
            The total duration of the right
        '''
        return self.get_end_time() - self.get_start_time()
    
    def _construct_filter_string(self, filters: Dict[str, Any]) -> str:
        prepped_filters = []
        for key, f in filters.items():
            filter = ''
            if type(f) is str:
                filter = f'{key}: "{f}"'
            else:
                filter = f'{key}: {f}'
            prepped_filters.append(filter)

        return ', '.join(prepped_filters)
    
    def _prepare_data_filters(self, filters: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
        fight_start, fight_end = self.get_start_time(), self.get_end_time()

        # defaulting for start/end times.
        # also check that if custom start/end times were supplied, they are within the fight
        if 'startTime' not in filters:
            filters['startTime'] = fight_start
        else:
            if filters['startTime'] < fight_start:
                raise ValueError('Cannot retrieve fight events before the fight has started!')
        if 'endTime' not in filters:
            filters['endTime'] = fight_end
        else:
            if filters['endTime'] > fight_end:
                raise ValueError('Cannot retrieve fight events after the fight has ended!')

        return self._construct_filter_string(filters), filters
    
    def get_fight_events(self, filters: Dict[str, Any] = {}) -> Dict[Any, Any]:
        '''
        Retrieves the events of the fight.

        If start/end time is not specified in filters, the default is the start/end of the fight.

        Args:
            filters: Key-value filters to filter the event log by. E.g. present/absent buffs, target IDs, etc.
        Returns:
            A dictionary of all events in the fight or None if the fight has zero duration
        '''
        if self.duration() == 0:
            return None

        filter_string, filters = self._prepare_data_filters(filters.copy())

        # used for pagination
        desired_end = filters['endTime']

        result = self.report._query_data(f'events({filter_string}) {{ data, nextPageTimestamp }}')
        fight_events = result['reportData']['report']['events']['data']

        # Check if there are more pages to this fight. If so, retrieve all of them and merge the data
        next_page = result['reportData']['report']['events']['nextPageTimestamp']
        while next_page and next_page < desired_end:
            time_range = filters['endTime'] - filters['startTime']
            filters['startTime'] = next_page
            filters['endTime'] = min(next_page + time_range, desired_end)

            filter_string = self._construct_filter_string(filters)
            result = self.report._query_data(f'events({filter_string}) {{ data, nextPageTimestamp }}')
            events = result['reportData']['report']['events']['data']
            fight_events += events
            next_page = result['reportData']['report']['events']['nextPageTimestamp']

        return fight_events

    def get_fight_graph(self, filters: Dict[str, Any] = {}) -> Dict[Any, Any]:
        '''
        Retrieves the graph information for the fight,
        i.e. damage done, healing done, etc. for various points in the fight.
        Shorter time intervals give higher point resolution.

        If start/end time is not specified in filters, the default is the start/end of the fight.

        Args:
            filters: Key-value filters to filter the graph by. E.g. present/absent buffs, target IDs, etc.
        Returns:
            A dictionary of graph information for the fight or None if the fight has zero duration
        '''
        if self.duration() == 0:
            return None

        graph_filters, _ = self._prepare_data_filters(filters.copy())

        result = self.report._query_data(f'graph({graph_filters})')
        return result['reportData']['report']['graph']

    def get_fight_table(self, filters: Dict[str, str] = {}) -> Dict[Any, Any]:
        '''
        Retrieves the table information for the fight.

        If start/end time is not specified in filters, the default is the start/end of the fight.

        Args:
            filters: Key-value filters to filter the table by. E.g. present/absent buffs, target IDs, etc.
        Returns:
            A dictionary of table information for the fight or None if the fight has zero duration
        '''
        if self.duration() == 0:
            return None

        table_filters, _ = self._prepare_data_filters(filters.copy())

        result = self.report._query_data(f'table({table_filters})')
        return result['reportData']['report']['table']['data']
    
    def get_rankings(self) -> Dict[Any, Any]:
        '''
        Retrieves ranking data for the fight.

        Returns:
            A dictionary of player ranking information.
        '''
        result = self.report._query_data(f'rankings(fightIDs: {self.fight_id})')
        return result['reportData']['report']['rankings']['data']

