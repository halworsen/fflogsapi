from typing import Optional

from .encounter import FFLogsEncounter
from .expansion import FFLogsExpansion
from .queries import Q_EXPANSION_LIST, Q_REGION_LIST, Q_ZONE_LIST
from .region import FFLogsRegion, FFLogsSubregion
from .server import FFLogsServer
from .zone import FFLogsZone


class WorldMixin:
    def get_encounter(self, id: int) -> FFLogsEncounter:
        '''
        Retrieves the given encounter data from FFLogs.

        Args:
            id: The encounter ID.
        Returns:
            A FFLogsEncounter object representing the encounter.
        '''
        return FFLogsEncounter(id=id, client=self)

    def get_expansion(self, id: int) -> FFLogsExpansion:
        '''
        Retrieves the given expansion data from FFLogs.

        Args:
            id: The expansion ID.
        Returns:
            A FFLogsExpansion object representing the expansion.
        '''
        return FFLogsExpansion(id=id, client=self)

    def get_all_expansions(self) -> list[FFLogsExpansion]:
        '''
        Retrieves a list of all expansions supported by FFLogs.

        Returns:
            A list of FFLogsExpansions representing each expansion.
        '''
        expacs = self.q(Q_EXPANSION_LIST.format(
            innerQuery='id',
        ))['worldData']['expansions']

        return [FFLogsExpansion(id=e['id'], client=self) for e in expacs]

    def get_region(self, id: int) -> FFLogsRegion:
        '''
        Retrieves the given region from FFLogs.

        Args:
            id: The region ID.
        Returns:
            A FFLogsRegion object representing the region.
        '''
        return FFLogsRegion(id=id, client=self)

    def get_all_regions(self) -> list[FFLogsRegion]:
        '''
        Retrieves a list of all regions supported by FFLogs.

        Returns:
            A list of FFLogsRegions representing each region.
        '''
        regions = self.q(Q_REGION_LIST.format(
            innerQuery='id',
        ))['worldData']['regions']

        return [FFLogsRegion(id=r['id'], client=self) for r in regions]

    def get_server(self, filters: dict = {}, id: Optional[int] = None) -> FFLogsServer:
        '''
        Retrieves server information from FFLogs given server filters.

        Args:
            filters: Optional filters to find the server by.
                     Valid filter fields are: id, region, slug. Default: {}
            id: The ID of the server to retrieve. Default: None
        Returns:
            A FFLogsServer object representing the server.
        '''
        if 'id' not in filters and id is not None:
            filters['id'] = id
        return FFLogsServer(filters=filters, client=self)

    def get_subregion(self, id: int) -> FFLogsSubregion:
        '''
        Retrieves the given subregion from FFLogs.

        Args:
            id: The subregion ID.
        Returns:
            A FFLogsSubregion object representing the subregion.
        '''
        return FFLogsSubregion(id=id, client=self)

    def get_zone(self, id: int) -> FFLogsZone:
        '''
        Retrieves the given zone from FFLogs.

        Args:
            id: The zone ID.
        Returns:
            A FFLogsZone object representing the zone.
        '''
        return FFLogsZone(id=id, client=self)

    def get_all_zones(self, expansion_id: int) -> list[FFLogsZone]:
        '''
        Retrieves a list of all zones belonging to a given expansion that are supported by FFLogs.

        Returns:
            A list of FFLogsZones representing each zone.
        '''
        zones = self.q(Q_ZONE_LIST.format(
            filters=f'expansion_id: {expansion_id}',
            innerQuery='id',
        ))['worldData']['zones']

        return [FFLogsZone(id=z['id'], client=self) for z in zones]
