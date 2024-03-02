from ...constants import EventType
from .phases import FightPhaseData, PhaseTransition, PhaseTransitionDefinition
from dataclasses import dataclass


@dataclass
class AlexanderPhaseData(FightPhaseData):
    encounter_id: int = 1062

    phases: tuple[str] = (
        'Living Liquid',
        'Brute Justice and Cruise Chaser',
        'Alexander Prime',
        'Perfect Alexander',
    )

    intermissions: tuple[str] = (
        'Limit Cut',
        'Temporal Stasis',
        'Inception Formation',
        'Wormhole Formation',
        'P4 Transition',
        'Fate Calibration Alpha',
        'Fate Calibration Beta',
    )

    phase_definitions: tuple[tuple[int, int, list[PhaseTransition]]] = (
        # LC
        PhaseTransitionDefinition(
            description='P1 ends, limit cut starts',
            game_id=2000032,
            event_def={'type': EventType.CAST.value, 'abilityGameID': 18480},
            transition_types=[PhaseTransition.END, PhaseTransition.INTERMISSION_START]
        ),

        # P2
        PhaseTransitionDefinition(
            description='Limit cut ends, P2 starts',
            game_id=11340,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END, PhaseTransition.START]
        ),

        # Temporal stasis
        PhaseTransitionDefinition(
            description='P2 ends, temporal stasis starts',
            game_id=11340,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.END, PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='Temporal stasis ends, P3 begins',
            game_id=11347,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END, PhaseTransition.START]
        ),

        # Inception
        PhaseTransitionDefinition(
            description='Inception formation begins',
            game_id=11347,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='Inception formation ends',
            game_id=11347,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # Wormhole
        PhaseTransitionDefinition(
            description='Wormhole formation begins',
            game_id=11347,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='Wormhole formation ends',
            game_id=11347,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # P4 transition
        PhaseTransitionDefinition(
            description='P3 ends, P4 transition begins',
            game_id=11347,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.END, PhaseTransition.INTERMISSION_START]
        ),

        # P4
        PhaseTransitionDefinition(
            description='Transition ends, P4 begins',
            game_id=11349,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.START, PhaseTransition.INTERMISSION_END]
        ),

        # Fate alpha
        PhaseTransitionDefinition(
            description='Fate calibration alpha begins',
            game_id=11349,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='Fate calibration alpha ends',
            game_id=11349,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # Fate beta
        PhaseTransitionDefinition(
            description='Fate calibration beta begins',
            game_id=11349,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='Fate calibration beta ends',
            game_id=11349,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),
    )
