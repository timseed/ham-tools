from collections import namedtuple
from unittest import TestCase
from unittest.mock import patch

from ham.equipment.elecraft.radio.p3 import P3
from .non_arduino_serial import NonArduinoSerial


class Test_p3(TestCase):
    @patch("ham.equipment.elecraft.radio.P3.open_serial")
    def setUp(self, fake_open_serial) -> None:
        fake_open_serial.return_value = NonArduinoSerial(port="COM99", baudrate=2400)
        self.p3 = P3(
            device="COMDOESNOTEXIST"
        )  # This Port does not matter - as have mocked the internal opening of Serial

    def test_avg(self):
        for n in range(2, 20):
            self.assertIsNone(self.p3.avg(n))
        # Test if raises for an out of value
        self.assertRaises(ValueError, self.p3.avg, **{"time_in_secs": 0})
        self.assertRaises(ValueError, self.p3.avg, **{"time_in_secs": 1})
        self.assertRaises(ValueError, self.p3.avg, **{"time_in_secs": 20})

    @patch("ham.equipment.elecraft.radio.P3.read")
    def test_avgq(self, fake_read):
        good_tests = {
            "#AVG02;": "02",
            "#AVG12;": "12",
            "#AVG19;": "19",
            "Umm;": "Unk",
        }
        for k, v in good_tests.items():
            fake_read.return_value = k
            self.assertEqual(self.p3.avgq(), v)

    def test_bmp(self):
        assert True

    def test_baud_rate(self):
        for speed in [1, 2, 3]:
            self.assertIsNone(self.p3.baud_rate(speed))
        # these should fail
        for speed in [4, 5, 6]:
            self.assertRaises(ValueError, self.p3.baud_rate, **{"speed": speed})

    def test_centre_freq(self):
        for f in [0, 14060, 14060.123, 28500.123]:
            self.assertIsNone(self.p3.centre_freq(f))

        for f in [31000.123, 45000]:
            self.assertRaises(ValueError, self.p3.centre_freq, **{"freq_in_hz": f})

    @patch("ham.equipment.elecraft.radio.P3.read")
    def test_centre_freqq(self, fake_read):
        good_tests = {
            "CTF+00014060000;": 14060.0,
            "CTF+00014060100;": 14060.1,
            "CTF+00014060110;": 14060.11,
        }
        for k, v in good_tests.items():
            fake_read.return_value = k
            self.assertEqual(v, self.p3.centre_freqq())

    def test_display_mode(self):
        for mode in [0, 1]:
            self.assertIsNone(self.p3.display_mode(mode))
        # these should fail
        for mode in [2, 3, 4]:
            self.assertRaises(ValueError, self.p3.display_mode, **{"mode": mode})

    @patch("ham.equipment.elecraft.radio.P3.read")
    def test_display_modeq(self, fake_read):
        good_tests = {
            "DSM0;": "spectrum",
            "DSM1;": "spectrum/waterfall",
            "D;": "Unk",
        }
        for k, v in good_tests.items():
            fake_read.return_value = k
            self.assertEqual(v, self.p3.display_modeq())

    def test_nb(self):
        self.assertIsNone(self.p3.nb(0))
        self.assertIsNone(self.p3.nb(1))
        self.assertRaises(ValueError, self.p3.nb, **{"on_off": 2})

    @patch("ham.equipment.elecraft.radio.P3.read")
    def test_nbq(self, fake_read):
        good_tests = {
            "NB0;": "off",
            "NB0;": "off",
            "N;": "Unk",
        }
        for k, v in good_tests.items():
            fake_read.return_value = k
            self.assertEqual(v, self.p3.nbq())
