'''
Custom implementation of tracking phases in fights such as ultimates
'''

from .phases import PhaseType, PhaseInformation
from .omega import OmegaPhaseData
from .alexander import AlexanderPhaseData

# I'm not super happy with these being singletons
# Should look into a better way to handle this
OmegaPhaseData = OmegaPhaseData()
AlexanderPhaseData = AlexanderPhaseData()

ALL_PHASE_DATA = [
    OmegaPhaseData,
    AlexanderPhaseData,
]

__all__ = [
    # phases.py
    'PhaseType',
    'PhaseInformation',

    # omega.py
    'OmegaPhaseData',

    # alexander.py
    'AlexanderPhaseData',

    'ALL_PHASE_DATA',
]
