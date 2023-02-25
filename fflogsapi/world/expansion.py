'''
The expansion module contains the class definitions for expansions, zones and encounters.
FFLogs' hierarchy for these is expansion -> zone -> encounter.
'''

from typing import TYPE_CHECKING, Any

from fflogsapi.util.indexing import itindex
from ..util.decorators import fetch_data
from ..util.filters import construct_filter_string
from .queries import Q_ENCOUNTER, Q_EXPANSION, Q_ZONE

if TYPE_CHECKING:
    from ..client import FFLogsClient

class FFLogsExpansion:
    '''
    Representation of an expansion on FFLogs.
    '''

    DATA_INDICES = ['worldData', 'expansion']

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self._id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a expansion
        '''
        result = self._client.q(Q_EXPANSION.format(
            expansionID=self._id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def id(self) -> int:
        '''
        Get the expansion's ID.

        Returns:
            The expansion's ID.
        '''
        return self._id

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the expansion's name.

        Returns:
            The expansion's name.
        '''
        return self._data['name']

    def zones(self) -> list['FFLogsZone']:
        '''
        Get a list of all zones within this expansion.

        Returns:
            A list of the expansion's zones.
        '''
        zones = self._query_data('zones{ id }')
        zone_ids = [e['id'] for e in zones['worldData']['expansion']['zones']]

        return [FFLogsZone(id=id, client=self._client) for id in zone_ids]

class FFLogsZone:
    '''
    Representation of a zone on FFLogs.
    '''

    DATA_INDICES = ['worldData', 'zone']

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self._id = id
        self._data = {'id': id}
        self._encounters = {}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a zone
        '''
        result = self._client.q(Q_ZONE.format(
            zoneID=self._id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def id(self) -> int:
        '''
        Get the zone's ID.

        Returns:
            The zone's ID.
        '''
        return self._id

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the zone's name.

        Returns:
            The zone's name.
        '''
        return self._data['name']

    @fetch_data('frozen')
    def frozen(self) -> str:
        '''
        Get whether or not data about the zone has been permanently frozen.

        Returns:
            Whether or not the zone is frozen.
        '''
        return self._data['frozen']

    def encounters(self) -> list['FFLogsEncounter']:
        '''
        Get a list of all encounters within this zone.

        Returns:
            A list of the zone's encounters.
        '''
        encounters = self._query_data('encounters{ id }')
        encounter_ids = [e['id'] for e in encounters['worldData']['zone']['encounters']]

        return [FFLogsEncounter(id=id, client=self._client) for id in encounter_ids]

    def brackets(self) -> dict:
        '''
        Get bracket information about the zone.

        Returns:
            The zone's bracket information.
        '''
        bracket_info = self._query_data('brackets{ type, min, max, bucket }')
        return bracket_info['worldData']['zone']['brackets']

    def partitions(self) -> dict:
        '''
        Get partition information about the zone.

        Returns:
            The zone's partition information.
        '''
        partition_info = self._query_data('partitions{ id, name, compactName, default }')
        return partition_info['worldData']['zone']['partitions']

    def difficulties(self) -> dict:
        '''
        Get difficulty information about the zone.

        Returns:
            The zone's difficulty information.
        '''
        difficulty_info = self._query_data('difficulties{ id, name, sizes }')
        return difficulty_info['worldData']['zone']['difficulties']

    def expansion(self) -> FFLogsExpansion:
        '''
        Get the expansion to which this zone belongs.

        Returns:
            The expansion that this zone belongs to.
        '''
        expac_id = itindex(self._query_data('expansion{ id }'), self.DATA_INDICES)['expansion']['id']
        return FFLogsExpansion(id=expac_id, client=self._client)

class FFLogsEncounter:
    '''
    Representation of an encounter on FFLogs.
    '''

    DATA_INDICES = ['worldData', 'encounter']

    def __init__(self, id: int, client: 'FFLogsClient' = None) -> None:
        self._id = id
        self._data = {'id': id}
        self._client = client

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about an encounter
        '''
        result = self._client.q(Q_ENCOUNTER.format(
            encounterID=self._id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return result

    def id(self) -> int:
        '''
        Get the encounter's ID.

        Returns:
            The encounter's ID.
        '''
        return self._id

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the encounter's name.

        Returns:
            The encounter's name.
        '''
        return self._data['name']

    def zone(self) -> 'FFLogsZone':
        '''
        Get the zone the encounter is found in.

        Returns:
            The encounter's zone.
        '''
        zone_id = self._query_data('zone{ id }')
        return FFLogsZone(id=zone_id, client=self._client)

    def character_rankings(self, filters: dict[str, Any] = {}) -> dict:
        '''
        Get character/player ranking information for the encounter.
        Character ranking pagination for encounters must be handled by hand.

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, server, etc.
        Returns:
            The encounter's filtered character ranking data.
        '''
        filter_string = construct_filter_string(filters)
        if filter_string != '':
            filter_string = f'({filter_string})'

        result = self._query_data(f'characterRankings{filter_string}')
        if 'characterRankings' not in self._data:
            self._data['characterRankings'] = result['worldData']['encounter']['characterRankings']

        return self._data['characterRankings']

    def fight_rankings(self, filters: dict[str, Any] = {}) -> dict:
        '''
        Get fight rankings for the encounter.
        Fight ranking pagination for encounters must be handled by hand.

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, server, etc.
        Returns:
            The encounter's filtered fight ranking data.
        '''
        filter_string = construct_filter_string(filters)
        if filter_string != '':
            filter_string = f'({filter_string})'

        result = self._query_data(f'fightRankings{filter_string}')
        if 'fightRankings' not in self._data:
            self._data['fightRankings'] = result['worldData']['encounter']['fightRankings']

        return self._data['fightRankings']
