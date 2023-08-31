from typing import Optional

from .encounter import FFLogsEncounter
from .expansion import FFLogsExpansion
from .queries import Q_EXPANSION_LIST, Q_REGION_LIST, Q_ZONE_LIST
from .region import FFLogsRegion, FFLogsSubregion
from .server import FFLogsServer
from .zone import FFLogsZone


class WorldMixin:
    '''
    Client extensions to support world data exposed by the FF Logs API.
    '''

    def get_encounter(self, id: int) -> FFLogsEncounter:
        '''
        Retrieves the given encounter data from FF Logs.

        Args:
            id: The encounter ID.
        Returns:
            A FFLogsEncounter object representing the encounter.
        '''
        return FFLogsEncounter(id=id, client=self)

    def get_expansion(self, id: int) -> FFLogsExpansion:
        '''
        Retrieves the given expansion data from FF Logs.

        Args:
            id: The expansion ID.
        Returns:
            A FFLogsExpansion object representing the expansion.
        '''
        return FFLogsExpansion(id=id, client=self)

    def all_expansions(self) -> list[FFLogsExpansion]:
        '''
        Retrieves a list of all expansions supported by FF Logs.

        Returns:
            A list of FFLogsExpansions representing each expansion.
        '''
        expacs = self.q(Q_EXPANSION_LIST.format(
            innerQuery='id',
        ))['worldData']['expansions']

        return [FFLogsExpansion(id=e['id'], client=self) for e in expacs]

    def get_region(self, id: int) -> FFLogsRegion:
        '''
        Retrieves the given region from FF Logs.

        Args:
            id: The region ID.
        Returns:
            A FFLogsRegion object representing the region.
        '''
        return FFLogsRegion(id=id, client=self)

    def all_regions(self) -> list[FFLogsRegion]:
        '''
        Retrieves a list of all regions supported by FF Logs.

        Returns:
            A list of FFLogsRegions representing each region.
        '''
        regions = self.q(Q_REGION_LIST.format(
            innerQuery='id',
        ))['worldData']['regions']

        return [FFLogsRegion(id=r['id'], client=self) for r in regions]

    def get_server(self, filters: dict = {}, id: Optional[int] = -1) -> FFLogsServer:
        '''
        Retrieves server information from FF Logs given server filters.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/worlddata.doc.html

        Args:
            filters: Optional filters to find the server by.
            id: The ID of the server to retrieve.
        Returns:
            A FFLogsServer object representing the server.
        '''
        return FFLogsServer(filters=filters, id=id, client=self)

    def get_subregion(self, id: int) -> FFLogsSubregion:
        '''
        Retrieves the given subregion from FF Logs.

        Args:
            id: The subregion ID.
        Returns:
            A FFLogsSubregion object representing the subregion.
        '''
        return FFLogsSubregion(id=id, client=self)

    def get_zone(self, id: int) -> FFLogsZone:
        '''
        Retrieves the given zone from FF Logs.

        Args:
            id: The zone ID.
        Returns:
            A FFLogsZone object representing the zone.
        '''
        return FFLogsZone(id=id, client=self)

    def all_zones(self, expansion_id: int) -> list[FFLogsZone]:
        '''
        Retrieves a list of all zones belonging to a given expansion that are supported by FF Logs.

        Returns:
            A list of FFLogsZones representing each zone.
        '''
        zones = self.q(Q_ZONE_LIST.format(
            filters=f'expansion_id: {expansion_id}',
            innerQuery='id',
        ))['worldData']['zones']

        return [FFLogsZone(id=z['id'], client=self) for z in zones]
