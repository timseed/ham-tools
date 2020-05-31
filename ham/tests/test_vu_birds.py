from unittest import TestCase

from ham.mode.sat import VuBirds, SatFM


class TestVubirds(TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.vub = VuBirds()

    def test_class_ok(self):
        self.assertIsInstance(self.vub, VuBirds)

    def test_process_no_data2(self):
        sats = [
            SatFM(
                satname="AO51",
                downlink_freq=436.150,
                uplink_freq=144.200,
                ctss_code=0,
                activate_code=0,
            ),
        ]
        self.assertEqual(self.vub.process([]), self.vub.header)

    def test_with_no_activate(self):
        self.maxDiff = None
        sats = [
            SatFM(
                satname="AO51",
                downlink_freq=436.150,
                uplink_freq=144.200,
                ctss_code=0,
                activate_code=0,
            ),
        ]
        expected = """Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
1,AO51-A,436.160000,off,5.000000,,88.5,88.5,023,NN,FM,5.00,S,,,,,
2,AO51-B,436.155000,off,5.000000,,88.5,88.5,023,NN,FM,5.00,S,,,,,
3,AO51-C,436.150000,off,5.000000,,88.5,88.5,023,NN,FM,5.00,S,,,,,
4,AO51-D,436.145000,off,5.000000,,88.5,88.5,023,NN,FM,5.00,S,,,,,
5,AO51-E,436.140000,off,5.000000,,88.5,88.5,023,NN,FM,5.00,S,,,,,
"""
        rv = self.vub.process(sats)
        if rv != expected:
            self.fail()

    def test_with_activate(self):
        self.maxDiff = None
        sats = [
            SatFM(
                satname="AO51",
                downlink_freq=436.150,
                uplink_freq=144.200,
                ctss_code=67.0,
                activate_code=97.0,
            ),
        ]
        expected = """Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
1,AO51-Arm,436.160000,off,5.000000,Tone,97.0,97.0,023,NN,FM,5.00,S,,,,,
2,AO51-A,436.160000,off,5.000000,Tone,67.0,67.0,023,NN,FM,5.00,S,,,,,
3,AO51-B,436.155000,off,5.000000,Tone,67.0,67.0,023,NN,FM,5.00,S,,,,,
4,AO51-C,436.150000,off,5.000000,Tone,67.0,67.0,023,NN,FM,5.00,S,,,,,
5,AO51-D,436.145000,off,5.000000,Tone,67.0,67.0,023,NN,FM,5.00,S,,,,,
6,AO51-E,436.140000,off,5.000000,Tone,67.0,67.0,023,NN,FM,5.00,S,,,,,
"""
        if self.vub.process(sats) != expected:
            self.fail()

    def test_simple_doppler(self):
        """

        :return:
        """
        self.assertEqual(self.vub.simple_doppler("ARM", 436.800), 436.810)
        self.assertEqual(self.vub.simple_doppler("A", 436.800), 436.810)
        self.assertEqual(self.vub.simple_doppler("B", 436.800), 436.805)
        self.assertEqual(self.vub.simple_doppler("C", 436.800), 436.800)
        self.assertEqual(self.vub.simple_doppler("D", 436.800), 436.795)
        self.assertEqual(self.vub.simple_doppler("E", 436.800), 436.790)
