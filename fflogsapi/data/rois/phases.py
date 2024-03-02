'''
Compute information about phased fights (like ultimates) that is not exposed by the FF Logs API
'''

from typing import TYPE_CHECKING
from dataclasses import dataclass
from enum import Enum

from ...util.gql_enums import GQLEnum
from queue import Queue

if TYPE_CHECKING:
    from ...reports import FFLogsFight


class PhaseType(Enum):
    PHASE = 'phase'
    '''Combat phase'''
    INTERMISSION = 'intermission'
    '''Intermission'''


class PhaseTransition(Enum):
    START = 'start'
    END = 'end'
    INTERMISSION_START = 'intermission start'
    INTERMISSION_END = 'intermission end'


@dataclass
class PhaseInformation:
    '''Name, timestamps and type of a fight phase'''

    type: PhaseType
    '''The type of phase. Either PhaseType.PHASE or PhaseType.INTERMISSION'''
    name: str = 'N/A'
    '''Pretty name of the phase or intermission'''
    start: int = -1
    '''Millisecond precision timestamp of when the phase starts, relative to the report start'''
    end: int = -1
    '''Millisecond precision timestamp of when the phase ends, relative to the report start'''


@dataclass
class PhaseTransitionDefinition:
    '''A set of information that determines when and how phase transitions occur'''

    description: str
    '''
    Human-readable description of what kind of transition this is.
    Mostly just to keep large lists of :class:`PhaseTransitionDefinition`s readable.
    '''

    game_id: int
    '''Game ID of the actor/boss that is the source of the phase defining event'''

    event_def: dict
    '''
    A dictionary that, at the bare minimum, contains a "type" field to filter event type with.
    Any other fields are used to determine which event defines the transition
    '''

    transition_types: list[PhaseTransition]
    '''A list of phase transition types that occur when the event defined by ``event_def`` occurs'''


@dataclass
class FightPhaseData:
    encounter_id: int
    '''The encounter which this phase data applies for'''

    phases: tuple[str]
    '''Ordered names of all phases'''
    intermissions: tuple[str]
    '''Ordered names of all intermissions'''

    phase_definitions: tuple[PhaseTransitionDefinition]
    '''An ordered list of information to define the start and end of different phases.'''

    def total_phases(self) -> int:
        '''
        Returns:
            The total amount of phases, including intermissions
        '''
        return len(self.phases) + len(self.intermissions)

    def get_phases(self, fight: 'FFLogsFight') -> list[PhaseInformation]:
        '''
        Iteratively searches for the next phase defining event in the fight's event log,
        creating new phase information in each iteration to construct a list of information
        on every phase in the fight.

        Args:
            fight: The :class:`FFLogsFight` to extract phase information from
        Returns:
            A list of :class:`PhaseInformation`s with information on all the different phases
            in the fight.
        '''
        fight_start = fight.start_time()
        fight_end = fight.end_time()
        game_id_map = {actor.id: actor.game_id for actor in fight.report.actors()}

        phases = []

        phase_idx, intermission_idx = 0, 0
        phase_start, phase_end = fight_start, 0
        intermission_start, intermission_end = 0, 0

        def_queue = Queue()
        for definition in self.phase_definitions:
            def_queue.put(definition)
        phase_def: PhaseTransitionDefinition = def_queue.get()

        filter_types = []
        for definition in self.phase_definitions:
            filter_types.append(definition.event_def['type'])
        filter_types = set(filter_types)

        done = False
        while not done:
            # refetching events and parsing the event log iteratively as we progress
            # is much much faster than fetching the full event log and then parsing
            events = fight.events(filters={
                'filterExpression': f'type = "{phase_def.event_def["type"]}"',
                'hostilityType': GQLEnum('Enemies'),
                'startTime': max(phase_start, intermission_start),
            })

            # trawl through all events leading up to the next phase transition event we expect
            done = True
            for event in events:
                game_id = game_id_map[event['sourceID']]

                # check if the event's boss gameID matches
                if game_id != phase_def.game_id:
                    continue
                # then check if the rest of the event matches by checking
                # if the event definition is a subset of the event
                if not (phase_def.event_def.items() <= event.items()):
                    continue

                # check what types of phase transitions the event corresponds to
                # phases are recorded when they end
                timestamp = event['timestamp']
                for transition in phase_def.transition_types:
                    if transition == PhaseTransition.START:
                        phase_start = timestamp
                    elif transition == PhaseTransition.INTERMISSION_START:
                        intermission_start = timestamp
                    elif transition == PhaseTransition.END:
                        phase_end = timestamp
                        phases.append(PhaseInformation(
                            type=PhaseType.PHASE,
                            name=self.phases[phase_idx],
                            start=phase_start, end=phase_end,
                        ))
                        phase_idx += 1
                    elif transition == PhaseTransition.INTERMISSION_END:
                        intermission_end = timestamp
                        phases.append(PhaseInformation(
                            type=PhaseType.INTERMISSION,
                            name=self.intermissions[intermission_idx],
                            start=intermission_start, end=intermission_end,
                        ))
                        intermission_idx += 1

                # finished processing the last phase defining event
                if def_queue.empty():
                    break

                # move on to the next phase defining event
                old_event_type = phase_def.event_def['type']
                phase_def = def_queue.get()
                # if the next phase defining event type is different,
                # break out so we can retrieve new events
                if phase_def.event_def['type'] != old_event_type:
                    done = False
                    break

        # manually insert phases if we were in the middle of one when the fight ended
        if phase_start >= phase_end and (phase_start + phase_end) != 0:
            phases.append(PhaseInformation(
                type=PhaseType.PHASE,
                name=self.phases[phase_idx],
                start=phase_start, end=fight_end,
            ))

        if intermission_start >= intermission_end and (intermission_start + intermission_end) != 0:
            phases.append(PhaseInformation(
                type=PhaseType.INTERMISSION,
                name=self.intermissions[intermission_idx],
                start=intermission_start, end=fight_end,
            ))

        # sort the list by start time
        # if a phase and intermission start at the same time, the phase start gets precedence
        phases.sort(key=lambda phase: phase.start + (0 if phase.type == PhaseType.PHASE else 1))
        return phases
