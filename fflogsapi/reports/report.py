from typing import TYPE_CHECKING, Iterator, Optional

from ..characters.character import FFLogsCharacter
from ..data import FFLogsActor, FFLogsArchivalData, FFLogsReportAbility, FFLogsReportTag
from ..user.user import FFLogsUser
from ..util.decorators import fetch_data
from ..util.indexing import itindex
from ..world.region import FFLogsRegion
from ..world.zone import FFLogsZone
from .fight import FFLogsFight
from .queries import IQ_REPORT_ABILITIES, IQ_REPORT_ACTORS, IQ_REPORT_LOG_VERSION, Q_REPORT_DATA

if TYPE_CHECKING:
    from ..client import FFLogsClient
    from ..guilds.guild import FFLogsGuild


class FFLogsReport:
    '''
    Representation of a report on FF Logs.
    '''

    DATA_INDICES = ['reportData', 'report']

    code: str = ''
    ''' The code for this report '''

    def __init__(self, code: str, client: 'FFLogsClient' = None) -> None:
        self.code = code
        self._fights = {}
        self._data = {}
        self._client = client

    def __iter__(self) -> Iterator:
        return iter(self.fights())

    def _query_data(self, query: str, ignore_cache: bool = False) -> None:
        '''
        Query for a specific piece of information from a report.
        '''
        result = self._client.q(Q_REPORT_DATA.format(
            reportCode=self.code,
            innerQuery=query
        ), ignore_cache=ignore_cache)

        return itindex(result, self.DATA_INDICES)

    def actors(self) -> list[FFLogsActor]:
        '''
        Returns:
            A list of all actors in the report
        '''
        if 'masterActors' not in self._data:
            actors = self._query_data(IQ_REPORT_ACTORS)['masterData']['actors']
            actors = sorted(actors, key=lambda a: a['id'])

            all_actors = {}
            for actor in actors:
                jobs = self._client.jobs()
                actor_job = list(filter(lambda j: j.slug == actor['subType'], jobs))
                actor = FFLogsActor(
                    report=self,
                    id=actor['id'],
                    name=actor['name'],
                    type=actor['type'],
                    sub_type=actor['subType'],
                    server=actor['server'],
                    game_id=actor['gameID'],
                    job=actor_job[0] if len(actor_job) else None,
                    pet_owner=None,
                )
                all_actors[actor.id] = actor

            # 2nd pass to fill pet owner fields with actual FFLogsActors instead of just IDs
            for actor in actors:
                if actor['petOwner'] is None:
                    continue
                all_actors[actor['id']].pet_owner = all_actors[actor['petOwner']]

            self._data['masterActors'] = list(all_actors.values())

        return self._data['masterActors']

    def actor(self, id: int) -> Optional[FFLogsActor]:
        '''
        Get a specific actor by their report ID.

        Args:
            id: The report ID of the actor.
        Returns:
            An actor or None if there is no actor with the given ID.
        '''
        # side effect to get actor data
        actors = self.actors()
        actors = list(filter(lambda a: a.id == id, actors))
        return (actors[0] if len(actors) else None)

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

    def archivation_data(self) -> FFLogsArchivalData:
        '''
        Get the archivation status for this report, including archival date, if any.

        Returns:
            The report's archivation data.
        '''
        data = self._query_data(
            'archiveStatus{ isArchived, isAccessible, archiveDate }'
        )['archiveStatus']

        return FFLogsArchivalData(
            archived=data['isArchived'],
            accessible=data['isAccessible'],
            date=data['archiveDate'],
        )

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
        '''
        Returns:
            The start timestamp of the report.
        '''
        return self._data['startTime']

    @fetch_data('endTime')
    def end_time(self) -> float:
        '''
        Returns:
            The end timestamp of the report.
        '''
        return self._data['endTime']

    @fetch_data('segments')
    def segments(self) -> int:
        '''
        Returns:
            The amount of segments uploaded to this report.
        '''
        return self._data['segments']

    @fetch_data('exportedSegments')
    def exported_segments(self) -> int:
        '''
        Returns:
            The amount of segments in this report that were exported.
        '''
        return self._data['exportedSegments']

    @fetch_data('visibility')
    def visibility(self) -> str:
        '''
        Get the visibility level of the report. Can be `public`, `private` or `unlisted`.

        Returns:
            The visibility of the report.
        '''
        return self._data['visibility']

    @fetch_data('revision')
    def revision(self) -> int:
        '''
        Get the report's revision number, which is increased every time the report is re-exported.

        Returns:
            The report's revision number.
        '''
        return self._data['revision']

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
        Get a specific fight from this report.

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

    def fights(self) -> list[FFLogsFight]:
        '''
        Returns:
            A list of all fights in this report.
        '''
        if len(self._fights) < self.fight_count():
            for id in range(1, self.fight_count() + 1):
                # fight() will update _fights as a side effect
                self.fight(id=id)
        return self._fights.values()

    def ranked_characters(self) -> list[FFLogsCharacter]:
        '''
        Get all the characters that ranked on kills in this report.

        Returns:
            A list of all ranked characters.
        '''
        if 'rankedCharacters' not in self._data:
            characters = self._query_data('rankedCharacters{ id }')['rankedCharacters']
            self._data['rankedCharacters'] = [
                FFLogsCharacter(id=id, client=self._client) for id in characters
            ]

        return self._data['rankedCharacters']
