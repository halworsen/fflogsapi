from typing import TYPE_CHECKING, Any

from ..util.decorators import fetch_data
from ..util.indexing import itindex
from .queries import Q_ZONE

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from .encounter import FFLogsEncounter
    from .expansion import FFLogsExpansion


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
        from .encounter import FFLogsEncounter

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

    def expansion(self) -> 'FFLogsExpansion':
        '''
        Get the expansion to which this zone belongs.

        Returns:
            The expansion that this zone belongs to.
        '''
        from .expansion import FFLogsExpansion

        result = self._query_data('expansion{ id }')
        expac_id = itindex(result, self.DATA_INDICES)['expansion']['id']
        return FFLogsExpansion(id=expac_id, client=self._client)
