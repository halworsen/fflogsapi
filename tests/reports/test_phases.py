import unittest

from fflogsapi import FFLogsClient
from fflogsapi.data import PhaseType, OmegaPhaseData, AlexanderPhaseData

from ..config import CACHE_EXPIRY, CLIENT_ID, CLIENT_SECRET


class FightTest(unittest.TestCase):
    '''
    Test cases for fight phases.

    This test case makes assumptions on the availability of specific reports.
    If the tests break, it may be because visibility settings
    were changed or the reports were deleted.
    '''

    # report codes and select fight ids: kill, somewhere in the middle, p1 and last phase wipe
    TOP_REPORT = ('ZLHv7rfd1RAQMWaV', 20, 1, 17, 4)
    TEA_REPORT = ('xdkpfmtDGMzrH6Ka', 11, 4, 7, 8)

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = FFLogsClient(CLIENT_ID, CLIENT_SECRET, cache_expiry=CACHE_EXPIRY)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.client.save_cache()

    def test_top(self) -> None:
        '''
        The client should be able to extract phase information from TOP fights
        '''
        # All phases and intermissions in order
        all_phases = (
            'Omega',
            'Omega M/F',
            'Party Synergy',
            'Omega Reconfigured',
            'P3 Transition',
            'Blue Screen',
            'P5 Transition',
            'Run: Dynamis',
            'Run: ****mi* (Delta)',
            'Run: ****mi* (Sigma)',
            'Run: ****mi* (Omega)',
            'P6 Transition',
            'Alpha Omega',
        )

        top_report = self.client.get_report(self.TOP_REPORT[0])

        # Test kill
        top_fight = top_report.fight(self.TOP_REPORT[1])
        phases = top_fight.phases()
        # 6 phases and 7 intermissions in total
        self.assertEqual(len(phases), OmegaPhaseData.total_phases())
        self.assertEqual(phases[0].start, top_fight.start_time())
        self.assertEqual(phases[-1].end, top_fight.end_time())

        # make sure all phases are accounted for and in correct order
        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(phase_names, all_phases)

        # Test wipe on P4 (somewhere in the middle)
        top_fight = top_report.fight(self.TOP_REPORT[2])
        phases = top_fight.phases()
        self.assertEqual(len(phases), 6)
        self.assertEqual(phases[0].start, top_fight.start_time())
        self.assertEqual(phases[-1].end, top_fight.end_time())

        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(
            phase_names,
            (
                'Omega',
                'Omega M/F',
                'Party Synergy',
                'Omega Reconfigured',
                'P3 Transition',
                'Blue Screen',
            )
        )

        # Test a phase 1 wipe
        top_fight = top_report.fight(self.TOP_REPORT[3])
        phases = top_fight.phases()
        self.assertEqual(len(phases), 1)
        self.assertEqual(phases[0].start, top_fight.start_time())
        self.assertEqual(phases[-1].end, top_fight.end_time())

        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(phase_names, ('Omega',))

        # Test a phase 6 wipe
        top_fight = top_report.fight(self.TOP_REPORT[4])
        phases = top_fight.phases()
        self.assertEqual(len(phases), OmegaPhaseData.total_phases())
        self.assertEqual(phases[0].start, top_fight.start_time())
        self.assertEqual(phases[-1].end, top_fight.end_time())

        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(phase_names, all_phases)

    def test_tea(self) -> None:
        '''
        The client should be able to extract phase information from TEA fights
        '''
        all_phases = (
            'Living Liquid',
            'Limit Cut',
            'Brute Justice and Cruise Chaser',
            'Temporal Stasis',
            'Alexander Prime',
            'Inception Formation',
            'Wormhole Formation',
            'P4 Transition',
            'Perfect Alexander',
            'Fate Calibration Alpha',
            'Fate Calibration Beta',
        )

        tea_report = self.client.get_report(self.TEA_REPORT[0])

        # Test kill
        tea_fight = tea_report.fight(self.TEA_REPORT[1])
        phases = tea_fight.phases()
        self.assertEqual(len(phases), AlexanderPhaseData.total_phases())
        self.assertEqual(phases[0].start, tea_fight.start_time())
        self.assertEqual(
            list(filter(lambda p: p.type == PhaseType.PHASE, phases))[-1].end,
            tea_fight.end_time()
        )

        # make sure all phases are accounted for and in correct order
        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(phase_names, all_phases)

        # Test wipe on temporal stasis
        tea_fight = tea_report.fight(self.TEA_REPORT[2])
        phases = tea_fight.phases()
        self.assertEqual(len(phases), 4)
        self.assertEqual(phases[0].start, tea_fight.start_time())
        self.assertEqual(phases[-1].end, tea_fight.end_time())

        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(
            phase_names,
            (
                'Living Liquid',
                'Limit Cut',
                'Brute Justice and Cruise Chaser',
                'Temporal Stasis',
            )
        )

        # Test a phase 1 wipe
        tea_fight = tea_report.fight(self.TEA_REPORT[3])
        phases = tea_fight.phases()
        self.assertEqual(len(phases), 1)
        self.assertEqual(phases[0].start, tea_fight.start_time())
        self.assertEqual(
            list(filter(lambda p: p.type == PhaseType.PHASE, phases))[-1].end,
            tea_fight.end_time()
        )

        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(phase_names, ('Living Liquid',))

        # Test a phase 4 wipe just before fate alpha
        tea_fight = tea_report.fight(self.TEA_REPORT[4])
        phases = tea_fight.phases()
        self.assertEqual(len(phases), 9)
        self.assertEqual(phases[0].start, tea_fight.start_time())
        self.assertEqual(
            list(filter(lambda p: p.type == PhaseType.PHASE, phases))[-1].end,
            tea_fight.end_time()
        )

        phase_names = tuple(map(lambda p: p.name, phases))
        self.assertTupleEqual(
            phase_names,
            (
                'Living Liquid',
                'Limit Cut',
                'Brute Justice and Cruise Chaser',
                'Temporal Stasis',
                'Alexander Prime',
                'Inception Formation',
                'Wormhole Formation',
                'P4 Transition',
                'Perfect Alexander',
            )
        )


if __name__ == '__main__':
    unittest.main()
