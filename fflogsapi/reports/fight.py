from typing import TYPE_CHECKING, Any, Optional, Union
from warnings import warn

from fflogsapi.data import (FFGameZone, FFJobInvalid, FFLogsNPCData, FFLogsPhase,
                            FFLogsPlayerDetails, FFLogsReportCharacterRanking,
                            FFLogsReportComboRanking, FFLogsReportRanking, FFMap,)

from ..characters.character import FFLogsCharacter
from ..util.decorators import fetch_data
from ..util.filters import construct_filter_string
from ..util.indexing import itindex
from ..world.encounter import FFLogsEncounter
from .queries import Q_FIGHT_DATA

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from .report import FFLogsReport


class FFLogsFight:
    '''
    Representation of a single fight on FF Logs.
    '''

    DATA_INDICES = ['reportData', 'report', 'fights', 0]

    id: int = -1
    ''' The ID of the fight, within the report which this fight belongs to '''

    report: 'FFLogsReport' = None
    ''' The report which this fight belongs to '''

    def __init__(self, report: 'FFLogsReport', fight_id: int, client: 'FFLogsClient') -> None:
        self.report = report
        self.id = fight_id
        self._client = client
        self._data = {}

    def _query_data(self, query: str, ignore_cache: bool = False) -> dict[Any, Any]:
        '''
        Query for a specific piece of information from a fight
        '''
        result = self._client.q(Q_FIGHT_DATA.format(
            reportCode=self.report.code,
            fightID=self.id,
            innerQuery=query,
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

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

    @fetch_data('inProgress')
    def in_progress(self) -> bool:
        '''
        If the report is being live logged, the fight may be marked as in progress.
        When the entire fight has been uploaded, the fight will be marked as no longer in progress.

        Returns:
            Whether or not the fight is still in progress.
        '''
        return self._data['inProgress']

    @fetch_data('bossPercentage')
    def percentage(self) -> float:
        '''
        Returns:
            The minimum percentage of HP that was reached for the last boss in the fight
        '''
        return self._data['bossPercentage']

    @fetch_data('fightPercentage')
    def fight_percentage(self) -> float:
        '''
        Returns:
            The minimum percentage of the entire fight that was reached
        '''
        return self._data['fightPercentage']

    @fetch_data('lastPhaseAsAbsoluteIndex')
    def last_phase_absolute(self) -> int:
        '''
        Returns:
            The last phase the fight was in when it ended,
            counting from 0 and including intermissions
        '''
        return self._data['lastPhaseAsAbsoluteIndex']

    @fetch_data('lastPhaseIsIntermission')
    def last_phase_intermission(self) -> bool:
        '''
        Returns:
            Whether or not the last phase of the fight is an intermission
        '''
        return self._data['lastPhaseIsIntermission']

    @fetch_data('difficulty')
    def difficulty(self) -> Optional[int]:
        '''
        Usually not very descriptive, as difficulty level 100 covers a wide variety of content.

        Returns:
            The difficulty of the fight.
        '''
        return self._data['difficulty']

    @fetch_data('encounterID')
    def encounter(self) -> FFLogsEncounter:
        '''
        Returns:
            The encounter the fight was a part of.
        '''
        return FFLogsEncounter(id=self._data['encounterID'], client=self._client)

    @fetch_data('friendlyPlayers')
    def friendly_players(self) -> list[int]:
        '''
        Returns:
            The IDs of all friendly players in the fight
        '''
        return self._data['friendlyPlayers']

    @fetch_data('startTime')
    def start_time(self) -> float:
        '''
        Returns:
            Start time of the fight relative to the start time of the report
        '''
        return self._data['startTime']

    @fetch_data('endTime')
    def end_time(self) -> float:
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
        return self.end_time() - self.start_time()

    @fetch_data('completeRaid')
    def complete_raid(self) -> bool:
        '''
        Whether or not this fight represents a full raid start to finish, i.e. a 'complete raid'.

        Returns:
            Whether or not this is a complete raid.
        '''
        return self._data['completeRaid']

    def bounding_box(self) -> tuple[int, int, int, int]:
        '''
        Get the bounding box that encloses all player's positions throughout the fight.

        Returns:
            The bounding box of player positions as a tuple of the form (minX, minY, maxX, maxY).
        '''
        bb = self._query_data('boundingBox{ minX, minY, maxX, maxY }')['boundingBox']

        return (bb['minX'], bb['minY'], bb['maxX'], bb['maxY'])

    def _prepare_data_filters(self, filters: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        '''
        Turn a dictionary of filters into a GraphQL filter string

        Returns:
            A filter string usable in GQL queries

        Raises:
            ValueError if the filter attempts to get events out of the fight's time bounds
        '''
        fight_start, fight_end = self.start_time(), self.end_time()

        # defaulting for start/end times.
        # also check that if custom start/end times were supplied, they are within the fight
        if 'startTime' not in filters:
            filters['startTime'] = fight_start
        elif filters['startTime'] < fight_start:
            raise ValueError('Cannot retrieve fight events before the fight has started!')
        if 'endTime' not in filters:
            filters['endTime'] = fight_end
        elif filters['endTime'] > fight_end:
            raise ValueError('Cannot retrieve fight events after the fight has ended!')

        return construct_filter_string(filters), filters

    def events(self, filters: dict[str, Any] = {}) -> list[dict[str, Any]]:
        '''
        Retrieves the events of the fight.

        If start/end time is not specified in filters, the default is the start/end of the fight.

        This data isn't considered frozen by FF Logs and may therefore change without notice.

        For a full list of valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/report.doc.html

        Args:
            filters: Filters to use when retrieving event log data.
        Returns:
            A filtered list of all events in the fight or None if the fight has zero duration
        '''
        if self.duration() == 0:
            return None

        filter_string, filters = self._prepare_data_filters(filters.copy())

        # used for pagination
        desired_end = filters['endTime']

        result = self.report._query_data(f'events({filter_string}) {{ data, nextPageTimestamp }}')
        fight_events = result['events']['data']

        # Check if there are more pages to this fight.
        # If so, retrieve all of them and merge the data.
        next_page = result['events']['nextPageTimestamp']
        while next_page and next_page < desired_end:
            filters['startTime'] = next_page

            filter_string = construct_filter_string(filters)
            result = self.report._query_data(
                f'events({filter_string}) {{ data, nextPageTimestamp }}'
            )
            events = result['events']['data']
            fight_events += events
            next_page = result['events']['nextPageTimestamp']

        return fight_events

    def graph(self, filters: dict[str, Any] = {}) -> dict[Any, Any]:
        '''
        Retrieves the graph information for the fight,
        i.e. damage done, healing done, etc. for various points in the fight.
        Shorter time intervals give higher point resolution.

        If start/end time is not specified in filters, the default is the start/end of the fight.

        This data isn't considered frozen by FF Logs and may therefore change without notice.

        For a full list of valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/report.doc.html

        Args:
            filters: Filters to use when retrieving graph data.
        Returns:
            A dictionary of graph information for the fight or None if the fight has zero duration
        '''
        if self.duration() == 0:
            return None

        graph_filters, _ = self._prepare_data_filters(filters.copy())

        result = self.report._query_data(f'graph({graph_filters})')
        return result['graph']['data']

    def table(self, filters: dict[str, str] = {}) -> dict[Any, Any]:
        '''
        Retrieves the table information for the fight.

        If start/end time is not specified in filters, the default is the start/end of the fight.

        This data isn't considered frozen by FF Logs and may therefore change without notice.

        For a full list of valid filters see the API documentation:
        https://www.fflogs.com/v2-api-docs/warcraft/report.doc.html

        Args:
            filters: Filters to use when retrieving table data.
        Returns:
            A dictionary of table information for the fight or None if the fight has zero duration
        '''
        if self.duration() == 0:
            return None

        table_filters, _ = self._prepare_data_filters(filters.copy())

        result = self.report._query_data(f'table({table_filters})')
        return result['table']['data']

    def rankings(
        self,
        metric: str = 'default',
        compare: str = 'Rankings',
        timeframe: str = 'Today',
    ) -> Optional[FFLogsReportRanking]:
        '''
        Retrieves ranking data for the fight.

        This data isn't considered frozen by FF Logs and may therefore change without notice.

        Args:
            metric: The type of metric to retrieve rankings for. The following are supported:
                    `default`, `bossdps`, `bossrdps`, `dps`, `hps`, `rdps`, `tankhps`
            compare: What to compare against. `Rankings` and `Parses` are supported. `Parses` will
                     compare against all parses in a two week window.
            timeframe: The time frame to compare against. `Today` and `Historical` are supported.
        Returns:
            A dictionary of player ranking information or None if there is no ranking information
            for this fight.
        '''
        if 'rankings' not in self._data:
            ranks = self.report._query_data(
                f'rankings(fightIDs: {self.id}, playerMetric: {metric},\
                compare: {compare}, timeframe: {timeframe})'
            )['rankings']['data']

            if not len(ranks):
                self._data['rankings'] = None
                return None
            ranks = ranks[0]

            jobs = self._client.jobs()
            character_rankings = []
            combo_rankings = []
            for role, data in ranks['roles'].items():
                for ranking in data['characters']:
                    character = FFLogsCharacter(id=ranking['id'], client=self._client)
                    job = list(filter(lambda j: j.slug == ranking['class'], jobs))[0]

                    if 'id_2' in ranking:
                        # this is a tank/healer combination ranking
                        job_b = list(filter(lambda j: j.slug == ranking['class_2'], jobs))[0]
                        combo_rankings.append(FFLogsReportComboRanking(
                            type=role,
                            character_a=character,
                            character_b=FFLogsCharacter(id=ranking['id_2'], client=self._client),
                            job_a=job,
                            job_b=job_b,
                            amount=ranking['amount'],
                            rank=str(ranking['rank']),
                            best_rank=str(ranking['best']),
                            total_parses=ranking['totalParses'],
                            percentile=ranking['rankPercent'],
                        ))
                    else:
                        # this is an individual ranking
                        character_rankings.append(FFLogsReportCharacterRanking(
                            character=character,
                            job=job,
                            amount=ranking['amount'],
                            rank=str(ranking['rank']),
                            best_rank=str(ranking['best']),
                            total_parses=ranking['totalParses'],
                            percentile=ranking['rankPercent'],
                        ))

            self._data['rankings'] = FFLogsReportRanking(
                patch=ranks['bracketData'],
                bracket=ranks['bracket'],
                deaths=ranks['deaths'],
                damage_taken_not_tanks=ranks['damageTakenExcludingTanks'],
                character_rankings=character_rankings,
                combo_rankings=combo_rankings,
            )

        return self._data['rankings']

    def player_details(self) -> list[FFLogsPlayerDetails]:
        '''
        Get a list of player details such as each player's job, name and server for this fight.

        This data isn't considered frozen by FF Logs and may therefore change without notice.

        Returns:
            The player details for this fight.
        '''
        if 'playerDetails' not in self._data:
            details = self.report._query_data(
                f'playerDetails(fightIDs: {self.id})'
            )['playerDetails']['data']['playerDetails']
            jobs = self._client.jobs()

            self._data['playerDetails'] = []
            for role, players in details.items():
                for data in players:
                    job_slug = data['type']
                    try:
                        job = [j for j in jobs if j.slug == job_slug][0]
                    except IndexError:
                        invalid_job = FFJobInvalid()
                        invalid_job.slug = job_slug
                        job = invalid_job

                    details = FFLogsPlayerDetails(
                        id=data['id'],
                        actor=self.report.actor(id=data['id']),
                        guid=data['guid'],
                        name=data['name'],
                        server=data['server'],
                        job=job,
                        role=role,
                    )
                    self._data['playerDetails'].append(details)

        return self._data['playerDetails']

    def enemy_npcs(self) -> list[FFLogsNPCData]:
        '''
        Get a list of all enemy NPCs that appear in this fight.

        Returns:
            A list of enemy NPCs in the fight or None if there are none.
        '''
        npcs = self._query_data(
            'enemyNPCs{ gameID, groupCount, id, instanceCount }'
        )['enemyNPCs']

        if not len(npcs):
            return None

        return [FFLogsNPCData(
            id=npc['id'],
            actor=self.report.actor(id=npc['id']),
            hostile=True,
            game_id=npc['gameID'],
            group_count=npc['groupCount'],
            instance_count=npc['instanceCount'],
            pet_owner=None,
        ) for npc in npcs]

    def friendly_npcs(self) -> Optional[list[FFLogsNPCData]]:
        '''
        Get a list of all friendly NPCs that appear in this fight.

        Returns:
            A list of all friendly NPCs in the fight or None if there are none.
        '''
        npcs = self._query_data(
            'friendlyNPCs{ gameID, groupCount, id, instanceCount }'
        )['friendlyNPCs']

        if not len(npcs):
            return None

        return [FFLogsNPCData(
            id=npc['id'],
            actor=self.report.actor(id=npc['id']),
            hostile=False,
            game_id=npc['gameID'],
            group_count=npc['groupCount'],
            instance_count=npc['instanceCount'],
            pet_owner=None,
        ) for npc in npcs]

    def pets(self) -> list[FFLogsNPCData]:
        '''
        Get a list of all friendly pet NPCs that appear in this fight.

        Returns:
            All friendly pets in the fight.
        '''
        npcs = self._query_data(
            'friendlyPets{ gameID, groupCount, id, instanceCount, petOwner }'
        )['friendlyPets']

        return [FFLogsNPCData(
            id=npc['id'],
            actor=self.report.actor(id=npc['id']),
            hostile=False,
            game_id=npc['gameID'],
            group_count=npc['groupCount'],
            instance_count=npc['instanceCount'],
            pet_owner=self.report.actor(id=npc['petOwner']),
        ) for npc in npcs]

    def game_zone(self) -> FFGameZone:
        '''
        The in-game zone in which this fight took place.

        Returns:
            The game zone this fight takes place in.
        '''
        game_zone = self._query_data('gameZone{ id, name }')['gameZone']
        return FFGameZone(
            id=game_zone['id'],
            name=game_zone['name'],
        )

    def maps(self) -> list[FFMap]:
        '''
        Get a list of all the maps involved in this fight.

        Returns:
            All maps involved in the fight.
        '''
        maps = self._query_data('maps{ id }')['maps']
        return [self._client.map(id=map['id']) for map in maps]

    @fetch_data('encounterID')
    def phases(self) -> list[FFLogsPhase]:
        '''
        Get a list of phases in this fight.

        Returns:
            A list of phases
        '''
        # Awkward implementation, the API exposes phase info on the report
        # But we want to expose it at the fight level, so we have to communicate
        # backwards with the parent report for this information
        if 'phases' not in self._data:
            assert (self.report is not None)
            encounter_id = self._data['encounterID']
            self._data['phases'] = self.report._query_phases()[encounter_id]
        return self._data['phases']

    @fetch_data('lastPhase', 'lastPhaseAsAbsoluteIndex')
    def last_phase(
        self,
        ignore_intermissions: bool = True,
        as_dataclass: bool = False
    ) -> Union[int, FFLogsPhase]:
        '''
        Get the phase the fight was in when the fight ended.

        Args:
            ignore_intermissions: When True, the last non-intermission phase is returned
            as_dataclass: Return the last phase as a FFLogsPhase dataclass.
                          This will become standard in the future.
        Returns:
            The last phase the fight was in when it ended
        '''
        last_phase = self._data['lastPhase']
        if as_dataclass:
            if not ignore_intermissions:
                last_phase = self._data['lastPhaseAsAbsoluteIndex'] + 1
            for phase in self.phases():
                if phase.id == last_phase:
                    last_phase = phase
                    break
        else:
            warn(
                'integer returns from FFLogsFight.last_phase are deprecated. '
                'Pass as_dataclass=True to get the new dataclass return instead.',
                category=FutureWarning,
            )
        return last_phase
