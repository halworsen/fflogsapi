from typing import TYPE_CHECKING, Optional

from ..user.user import FFLogsUser
from ..util.decorators import fetch_data
from ..util.indexing import itindex
from ..world.region import FFLogsRegion
from ..world.zone import FFLogsZone
from .dataclasses import FFLogsActor, FFLogsReportAbility
from .fight import FFLogsFight
from .queries import IQ_REPORT_ABILITIES, IQ_REPORT_ACTORS, IQ_REPORT_LOG_VERSION, Q_REPORT_DATA

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from ..guilds.dataclasses import FFLogsReportTag
    from ..guilds.guild import FFLogsGuild


class FFLogsReport:
    '''
    Representation of a report on FFLogs.
    '''

    DATA_INDICES = ['reportData', 'report']

    def __init__(self, code: str, client: 'FFLogsClient' = None) -> None:
        self._code = code
        self._fights = {}
        self._data = {}
        self._client = client

    def __iter__(self) -> 'FFLogsReportIterator':
        return FFLogsReportIterator(report=self, client=self._client)

    def fights(self) -> list[FFLogsFight]:
        return list(self.__iter__())

    def _query_data(self, query: str, ignore_cache: bool = False) -> None:
        '''
        Query for a specific piece of information from a report.
        '''
        result = self._client.q(Q_REPORT_DATA.format(
            reportCode=self._code,
            innerQuery=query
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    def code(self) -> str:
        '''
        Returns:
            The report code
        '''
        return self._code

    def actors(self) -> list[FFLogsActor]:
        '''
        Returns:
            A list of all actors in the report
        '''
        if 'masterActors' not in self._data:
            actors = self._query_data(IQ_REPORT_ACTORS)['masterData']['actors']

            all_actors = []
            for actor in actors:
                jobs = self._client.jobs()
                actor_job = list(filter(lambda j: j.slug == actor['subType'], jobs))
                actor = FFLogsActor(
                    id=actor['id'],
                    name=actor['name'],
                    type=actor['type'],
                    sub_type=actor['subType'],
                    server=actor['server'],
                    game_id=actor['gameID'],
                    job=actor_job[0] if len(actor_job) else None,
                    pet_owner=actor['petOwner'],
                )

                all_actors.append(actor)

            self._data['masterActors'] = all_actors

        return self._data['masterActors']

    def abilities(self) -> list[FFLogsReportAbility]:
        '''
        Returns:
            A list of all abilities in the report
        '''
        if 'masterAbilities' not in self._data:
            abilities = self._query_data(IQ_REPORT_ABILITIES)['masterData']['abilities']

            all_abilities = []
            for ability in abilities:
                ability = FFLogsReportAbility(
                    game_id=ability['gameID'],
                    name=ability['name'],
                    type=ability['type'],
                )

                all_abilities.append(ability)

            self._data['masterAbilities'] = all_abilities

        return self._data['masterAbilities']

    def log_version(self) -> int:
        '''
        Returns:
            The version of the parser client used to parse and upload the log file.
        '''
        version = self._query_data(IQ_REPORT_LOG_VERSION)['masterData']['logVersion']
        return version

    @fetch_data('title')
    def title(self) -> str:
        '''
        Returns:
            The title of this report.
        '''
        return self._data['title']

    def owner(self) -> FFLogsUser:
        '''
        Returns:
            The user that owns this report.
        '''
        owner_id = self._query_data('owner{ id }')['owner']['id']
        return FFLogsUser(id=owner_id, client=self._client)

    def guild(self) -> Optional['FFLogsGuild']:
        '''
        Returns:
            The guild this report belongs to, if any.
        '''
        from ..guilds.guild import FFLogsGuild
        guild = self._query_data('guild{ id }')['guild']
        if guild is None:
            return None
        return FFLogsGuild(id=guild['id'], client=self._client)

    def tag(self) -> Optional['FFLogsReportTag']:
        '''
        The tag applied to this report used by the guild to which this report belongs. If a tag
        was not applied, returns None.

        Returns:
            The report tag, if any.
        '''
        from ..guilds.dataclasses import FFLogsReportTag
        tag = self._query_data('guildTag{ id, name }')['guildTag']
        if tag is None:
            return None
        return FFLogsReportTag(id=tag['id'], name=tag['name'], guild=self.guild())

    def zone(self) -> FFLogsZone:
        '''
        Returns:
            The principal zone for fights in this report.
        '''
        zone_id = self._query_data('zone{ id }')['zone']['id']
        return FFLogsZone(id=zone_id)

    def region(self) -> FFLogsRegion:
        '''
        Returns:
            The region of the report.
        '''
        id = self._query_data('region{ id }')['region']['id']
        return FFLogsRegion(id=id, client=self._client)

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
        return len(result['fights'])

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


class FFLogsReportIterator:
    '''
    Iterates over a report, returning fights
    '''

    def __init__(self, report: FFLogsReport, client: 'FFLogsClient') -> None:
        self._report = report
        self._client = client
        self._cur_encounter = 0
        self._max_encounter = report.fight_count()

    def __iter__(self) -> 'FFLogsReportIterator':
        return self

    def __next__(self) -> FFLogsFight:
        self._cur_encounter += 1
        if self._cur_encounter <= self._max_encounter:
            return self._report.fight(self._cur_encounter)
        else:
            self._cur_encounter = 0
            raise StopIteration
