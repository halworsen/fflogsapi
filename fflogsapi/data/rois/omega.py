from ...constants import EventType
from .phases import FightPhaseData, PhaseTransition, PhaseTransitionDefinition
from dataclasses import dataclass


@dataclass
class OmegaPhaseData(FightPhaseData):
    encounter_id: int = 1068

    phases: tuple[str] = (
        'Omega',
        'Omega M/F',
        'Omega Reconfigured',
        'Blue Screen',
        'Run: Dynamis',
        'Alpha Omega',
    )

    intermissions: tuple[str] = (
        'Party Synergy',
        'P3 Transition',
        'P5 Transition',
        'Run: ****mi* (Delta)',
        'Run: ****mi* (Sigma)',
        'Run: ****mi* (Omega)',
        'P6 Transition',
    )

    phase_definitions: tuple[tuple[int, int, list[PhaseTransition]]] = (
        # P2
        PhaseTransitionDefinition(
            description='P1 ends and P2 starts',
            game_id=15712,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.END, PhaseTransition.START]
        ),
        PhaseTransitionDefinition(
            description='P2 - Party synergy mechanic begins',
            game_id=15712,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='P2 - Party synergy mechanic ends',
            game_id=15712,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # P3
        PhaseTransitionDefinition(
            description='P2 ends, P3 starts with the transition mechanic',
            game_id=15712,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[
                PhaseTransition.END,
                PhaseTransition.START,
                PhaseTransition.INTERMISSION_START,
            ]
        ),
        PhaseTransitionDefinition(
            description='P3 transition ends, Omega becomes targetable',
            game_id=15717,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # Could add an intermission between P3-P4 but idk if there's any point as there's no damage

        # P4
        PhaseTransitionDefinition(
            description='P3 ends and P4 begins as Omega becomes targetable again',
            game_id=15717,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.END, PhaseTransition.START]
        ),

        # P5
        PhaseTransitionDefinition(
            description='P5 transition starts',
            game_id=15717,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),

        PhaseTransitionDefinition(
            description='P4 & P5 transition ends, P5 starts',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[
                PhaseTransition.END,
                PhaseTransition.INTERMISSION_END,
                PhaseTransition.START,
            ]
        ),

        # Dynamis delta
        PhaseTransitionDefinition(
            description='P5 - Run: ****mi* (Delta) begins',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='P5 - Run: ****mi* (Delta) ends',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # Dynamis sigma
        PhaseTransitionDefinition(
            description='P5 - Run: ****mi* (Sigma) begins',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='P5 - Run: ****mi* (Sigma) ends',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # Dynamis omega
        PhaseTransitionDefinition(
            description='P5 - Run: ****mi* (Omega) begins',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[PhaseTransition.INTERMISSION_START]
        ),
        PhaseTransitionDefinition(
            description='P5 - Run: ****mi* (Omega) ends',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),

        # P6
        PhaseTransitionDefinition(
            description='P5 ends and P6 transition begins',
            game_id=15720,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 0},
            transition_types=[
                PhaseTransition.END,
                PhaseTransition.INTERMISSION_START,
            ]
        ),

        PhaseTransitionDefinition(
            description='P6 begins with Omega-F casting Blind Faith',
            game_id=2000021,
            event_def={'type': EventType.CAST.value, 'abilityGameID': 32626},
            transition_types=[
                PhaseTransition.START,
            ]
        ),

        PhaseTransitionDefinition(
            description='P6 transition ends',
            game_id=15725,
            event_def={'type': EventType.TARGETABILITY_UPDATE.value, 'targetable': 1},
            transition_types=[PhaseTransition.INTERMISSION_END]
        ),
    )
