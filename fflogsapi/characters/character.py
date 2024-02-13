from typing import TYPE_CHECKING, Any, Optional, Union

from ..data import (FFJob, FFLogsAllStarsRanking, FFLogsEncounterRankings, FFLogsFightRank,
                    FFLogsZoneEncounterRanking, FFLogsZoneRanking,)
from ..util.decorators import fetch_data
from ..util.filters import construct_filter_string
from ..util.indexing import itindex
from .queries import Q_CHARACTER_DATA

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from ..guilds.guild import FFLogsGuild
    from ..world.server import FFLogsServer
    from ..world.zone import FFLogsZone


class FFLogsCharacter:
    '''
    Representation of a character on FFLogs.
    '''

    DATA_INDICES = ['characterData', 'character']

    id: int = -1
    ''' The ID of the character '''

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
        Query for a specific piece of information about a character
        '''
        filters = construct_filter_string(self.filters)
        result = self._client.q(Q_CHARACTER_DATA.format(
            filters=filters,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    @fetch_data('lodestoneID')
    def lodestone_id(self) -> int:
        '''
        Get the character's Lodestone ID.

        Returns:
            The character's Lodestone ID.
        '''
        return self._data['lodestoneID']

    @fetch_data('name')
    def name(self) -> str:
        '''
        Get the character's name.

        Returns:
            The character's name.
        '''
        return self._data['name']

    def server(self) -> 'FFLogsServer':
        '''
        Get the server the character belongs to.

        Returns:
            The character's server.
        '''
        from ..world.server import FFLogsServer
        server_id = self._query_data('server{ id }')['server']['id']
        return FFLogsServer(filters={'id': server_id}, client=self._client)

    @fetch_data('guildRank')
    def fc_rank(self) -> str:
        '''
        Get the FC rank of the character. This is game data, not FFLogs data.

        Returns:
            The character's FC rank.
        '''
        return self._data['guildRank']

    def guilds(self) -> list['FFLogsGuild']:
        '''
        Get a list of all guilds that this character belongs to.

        Returns:
            A list of guilds the character is in.
        '''
        from ..guilds.guild import FFLogsGuild
        guilds = self._query_data('guilds{ id }')['guilds']
        return [FFLogsGuild(id=guild['id'], client=self._client) for guild in guilds]

    def game_data(self, filters: dict = {}) -> dict:
        '''
        Get cached game data tied to the character, such as gear.

        Args:
            filters: Filter game data to a specific `specID` or force an update by the API with
                     `forceUpdate`.
        Returns:
            The character's game data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'gameData{filters}')
        return result['gameData']

    @fetch_data('hidden')
    def hidden(self) -> bool:
        '''
        Whether or not the character's rankings are hidden.

        Returns:
            True if the rankings are hidden, False otherwise.
        '''
        return self._data['hidden']

    def encounter_rankings(
            self,
            filters: dict[str, Any] = {},
    ) -> Union[dict, FFLogsEncounterRankings]:
        '''
        Get this character's rankings for a specific encounter. `encounterID` is mandatory.

        For valid filter fields, see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/character.doc.html

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, encounter ID, etc.
        Returns:
            The character's filtered ranking data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'encounterRankings{filters}')['encounterRankings']
        from ..guilds.guild import FFLogsGuild
        from ..reports.report import FFLogsReport
        jobs = self._client.jobs()
        ranks = []
        for rank in result['ranks']:
            report = FFLogsReport(code=rank['report']['code'], client=self._client)
            fight = report.fight(id=rank['report']['fightID'])

            guild = None
            if rank['guild']['id']:
                guild = FFLogsGuild(id=rank['guild']['id'], client=self._client)

            job = list(filter(lambda j: j.slug == rank['spec'], jobs))[0]
            best_job = list(filter(lambda j: j.slug == rank['bestSpec'], jobs))[0]

            ranks.append(FFLogsFightRank(
                locked_in=rank['lockedIn'],
                bracket_data=str(rank['bracketData']),
                fight=fight,
                guild=guild,
                job=job,
                best_job=best_job,
                rank_percent=rank['rankPercent'],
                rank_total_parses=rank['rankTotalParses'],
                historical_percent=rank['historicalPercent'],
                historical_total_parses=rank['historicalTotalParses'],
                today_percent=rank['todayPercent'],
                today_total_parses=rank['todayTotalParses'],
                adps=rank['aDPS'],
                rdps=rank['rDPS'],
                ndps=rank['nDPS'],
                pdps=rank['pDPS'],
            ))

        from ..world.zone import FFLogsZone
        return FFLogsEncounterRankings(
            zone=FFLogsZone(id=result['zone'], client=self._client),
            difficulty=result['difficulty'],
            metric=result['metric'],
            best_amount=result['bestAmount'],
            median_performance=result['medianPerformance'],
            average_performance=result['averagePerformance'],
            kills=result['totalKills'],
            fastest_kill=result['fastestKill'],
            ranks=ranks,
        )

    def _make_all_stars_ranking(
            self,
            data: dict,
            zone: 'FFLogsZone' = None,
            job: Optional[FFJob] = None,
    ) -> FFLogsAllStarsRanking:
        '''
        Turn JSON data into an all-stars ranking dataclass
        '''
        jobs = self._client.jobs()
        if not job and 'spec' in data:
            job = list(filter(lambda j: j.slug == data['spec'], jobs))[0]

        partitions = zone.partitions()
        return FFLogsAllStarsRanking(
            job=job,
            partition=next(filter(lambda p: p.id == data['partition'], partitions)),
            points=data['points'],
            possible_points=data['possiblePoints'],
            rank=data['rank'],
            region_rank=data['regionRank'],
            server_rank=data['serverRank'],
            rank_percent=data['rankPercent'],
            total=data['total']
        )

    def zone_rankings(
            self,
            filters: dict[str, Any] = {},
    ) -> Union[dict, FFLogsZoneRanking]:
        '''
        Get this character's rankings for a zone (boss).

        For valid filter fields, see the API documentation:
        https://www.fflogs.com/v2-api-docs/ff/character.doc.html

        Args:
            filters: Key-value filters to filter the rankings by. E.g. job name, zone ID, etc.
        Returns:
            The character's filtered ranking data.
        '''
        filters = construct_filter_string(filters)
        if filters:
            filters = f'({filters})'

        result = self._query_data(f'zoneRankings{filters}')['zoneRankings']
        from ..world.zone import FFLogsZone
        zone = FFLogsZone(id=result['zone'], client=self._client)
        jobs = self._client.jobs()
        encounters = []
        for rank in result['rankings']:
            # TODO: real fixes instead of ignoring the issue
            # IndexError is from the spec filters on null rankings
            # StopIteration is from the allstars ranking construction
            try:
                from ..world.encounter import FFLogsEncounter
                encounter = FFLogsEncounter(id=rank['encounter']['id'], client=self._client)
                job = list(filter(lambda j: j.slug == rank['spec'], jobs))[0]
                best_job = list(filter(lambda j: j.slug == rank['bestSpec'], jobs))[0]

                encounters.append(FFLogsZoneEncounterRanking(
                    locked_in=rank['lockedIn'],
                    encounter=encounter,
                    rank_percent=rank['rankPercent'],
                    median_percent=rank['medianPercent'],
                    best_amount=rank['bestAmount'],
                    fastest_kill=rank['fastestKill'],
                    kills=rank['totalKills'],
                    job=job,
                    best_job=best_job,
                    all_stars=self._make_all_stars_ranking(rank['allStars'], zone=zone, job=job),
                ))
            except (IndexError, StopIteration):
                continue

        return FFLogsZoneRanking(
            zone=zone,
            encounter_ranks=encounters,
            metric=result['metric'],
            difficulty=result['difficulty'],
            best_performance_avg=result['bestPerformanceAverage'],
            median_performance_avg=result['medianPerformanceAverage'],
            all_stars=[
                self._make_all_stars_ranking(alls, zone=zone) for alls in result['allStars']
            ],
        )
