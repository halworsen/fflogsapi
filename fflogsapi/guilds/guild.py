from typing import TYPE_CHECKING, Any, Union

from ..constants import FightDifficulty, PartySize
from ..data import FFGrandCompany, FFLogsGuildZoneRankings, FFLogsRank, FFLogsReportTag
from ..util.decorators import fetch_data
from ..util.filters import construct_filter_string
from ..util.indexing import itindex
from ..world.server import FFLogsServer
from ..world.zone import FFLogsZone
from .pages import FFLogsCharacterPaginationIterator, FFLogsGuildAttendancePaginationIterator
from .queries import Q_GUILD, Q_GUILD_RANKING

if TYPE_CHECKING:
    from ..client import FFLogsClient


class FFLogsGuild:
    '''
    FFLogs guild information object.
    '''

    DATA_INDICES = ['guildData', 'guild']

    id: int = -1
    ''' The ID of the guild '''

    def __init__(self, filters: dict = {}, id: int = -1, client: 'FFLogsClient' = None) -> None:
        self.filters = filters.copy()
        self._client = client
        self._data = {}

        if id != -1 and 'id' not in self.filters:
            self.filters['id'] = id
        else:
            result = self._query_data('id')
            self._data['id'] = result['id']
            self.filters = {'id': result['id']}

        self.id = self.filters['id']

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information about a guild
        '''
        filters = construct_filter_string(self.filters)
        result = self._client.q(Q_GUILD.format(
            filters=filters,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the name of the guild.

        Returns:
            The name of the guild.
        '''
        return self._data['name']

    @fetch_data('description')
    def description(self) -> str:
        '''
        Get the description of the guild.

        Returns:
            The description of the guild.
        '''
        return self._data['description']

    @fetch_data('type')
    def type(self) -> str:
        '''
        Get the type of the guild. A type of 0 indicates the guild is a Free Company, while a
        type of 1 indicates the guild is a Static.

        Returns:
            The type of the guild.
        '''
        return self._data['type']

    @fetch_data('competitionMode')
    def competition_mode(self) -> bool:
        '''
        Get whether or not the guild has competition mode enabled.

        Returns:
            The competition mode of the guild.
        '''
        return self._data['competitionMode']

    @fetch_data('stealthMode')
    def stealth_mode(self) -> bool:
        '''
        Get whether or not the guild has stealth mode enabled.

        Returns:
            The stealth mode of the guild.
        '''
        return self._data['stealthMode']

    @fetch_data('currentUserRank')
    def current_rank(self) -> str:
        '''
        Requires the API client to be in user mode.

        Gets the current user's rank in the guild. This is not ranking data.
        The rank can be `NonMember`, `Applicant`, `Recruit`, `Member`, `Officer` or `GuildMaster`.

        Returns:
            The user's rank in the guild.
        '''
        return self._data['currentUserRank']

    def server(self) -> FFLogsServer:
        '''
        Get the server to which this guild belongs.

        Returns:
            The server the guild belogns to
        '''
        id = self._query_data(query='server{ id }')['server']['id']
        return FFLogsServer(id=id, client=self._client)

    def tags(self) -> list[FFLogsReportTag]:
        '''
        Get a list of all the tags this guild uses to label its reports.

        Returns:
            The guild's tags.
        '''
        tags = self._query_data(query='tags{ id, name }')['tags']
        return [FFLogsReportTag(id=tag['id'], name=tag['name'], guild=self) for tag in tags]

    def grand_company(self) -> FFGrandCompany:
        '''
        Get the grand company to which this guild belongs.

        Returns:
            The grand company the guild belongs to.
        '''
        grand_company = self._query_data(query='faction{ id, name }')['faction']
        return FFGrandCompany(id=grand_company['id'], name=grand_company['name'])

    def attendance(self, filters: dict = {}) -> FFLogsGuildAttendancePaginationIterator:
        '''
        Get a pagination of attandance reports.

        For valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/guild.doc.html

        Args:
            filters: Zone and tag ID filters to filter attendance reports by.
        Returns:
            An iterator over all attendance report pages.
        '''
        return FFLogsGuildAttendancePaginationIterator(
            additional_formatting={'guildID': self.id},
            filters=filters,
            client=self._client,
        )

    def characters(self) -> FFLogsCharacterPaginationIterator:
        '''
        Get a pagination of all characters belonging to the guild.

        Returns:
            An iterator over all guild character pages.
        '''
        return FFLogsCharacterPaginationIterator(
            client=self._client,
            additional_formatting={'guildID': self.id}
        )

    def zone_rankings(
            self,
            zone: Union[int, FFLogsZone],
            size: int = PartySize.FULL.value,
            difficulty: int = FightDifficulty.SAVAGE.value,
    ) -> FFLogsGuildZoneRankings:
        '''
        Retrieve the guild's ranking information for a given zone, party size and difficulty.

        Args:
            zone: Either the `int` ID of the zone, or the zone to retrieve ranking information for.
            size: The party size for which to retrieve rankings.
            difficulty: The difficulty level for which to retrieve rankings.
        '''
        zone_id = -1
        if isinstance(zone, int):
            zone_id = zone
        elif isinstance(zone, FFLogsZone):
            zone_id = zone.id

        data = self._query_data(Q_GUILD_RANKING.format(
            zoneID=zone_id,
            size=size,
            difficulty=difficulty,
        ))['zoneRanking']

        for key in data.keys():
            if not data[key]:
                continue

            data[key] = tuple([
                FFLogsRank(
                    number=data[key]['worldRank']['number'],
                    color=data[key]['worldRank']['color'],
                    percentile=None,
                ),
                FFLogsRank(
                    number=data[key]['regionRank']['number'],
                    color=data[key]['regionRank']['color'],
                    percentile=None,
                ),
                FFLogsRank(
                    number=data[key]['serverRank']['number'],
                    color=data[key]['serverRank']['color'],
                    percentile=None,
                ),
            ])

        return FFLogsGuildZoneRankings(
            completion_speed=data['completeRaidSpeed'],
            progress=data['progress'],
            speed=data['speed'],
        )
