from collections import namedtuple
from unittest import TestCase
from unittest.mock import patch

from ham.equipment.elecraft.radio.k3 import K3
from .non_arduino_serial import NonArduinoSerial


class test_k3(TestCase):
    @patch("ham.equipment.elecraft.radio.K3.open_serial")
    def setUp(self, fake_open_serial) -> None:
        fake_open_serial.return_value = NonArduinoSerial(port="COM99", baudrate=2400)
        self.rig = K3(
            port="COMDOESNOTEXIST"
        )  # This Port does not matter - as have mocked the internal opening of Serial

    # def test_show_port(self):
    #     self.assertEqual(self.rig.show_port(), 'COM99')

    # def test_close(self):
    #     assert True
    #
    # def test_write(self):
    #     assert True

    # def test_read(self):
    #     assert True
    #
    @patch("ham.equipment.elecraft.radio.K3.qsyq")
    def test_qsy(self, fake_qsyq):
        good = {21050000: "21050000", 28030000: "28030000"}
        for k, v in good.items():
            fake_qsyq.return_value = v
            self.assertEqual(self.rig.qsy(k), v)

        bad = {123456789123: "0", 321987654321: "0"}

        for k, v in bad.items():
            fake_qsyq.return_value = v
            self.assertRaises(ValueError, self.rig.qsy, k)

    @patch("ham.equipment.elecraft.radio.K3.qsyq")
    def test_qsy2(self, fake_qsyq2):
        good = {21050000: "21050000", 28030000: "28030000"}
        for k, v in good.items():
            fake_qsyq2.return_value = v
            self.assertEqual(self.rig.qsy(k), v)

        bad = {123456789123: "0", 321987654321: "0"}

        for k, v in bad.items():
            fake_qsyq2.return_value = v
            self.assertRaises(ValueError, self.rig.qsy, k)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_fiq(self, fake_read):
        fake_read.return_value = "1234567"
        self.assertEqual(self.rig.fiq(), "8213.456")

        # Now lets return an invalid read
        fake_read.return_value = "2"
        self.assertEqual(self.rig.fiq(), "0")

    def test_nb(self):
        for thresh in range(0, 3):
            self.assertIsNone(self.rig.nb(1, thresh))

        # This should raise an errors
        for t in range(3, 10):
            self.assertRaises(ValueError, self.rig.nb, **{"level": 1, "thresh": t})

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_nbq(self, fake_read):
        good_tests = {
            "00000": "NB: 0 0",
            "00010": "NB: 0 1",
            "00022": "NB: 0 2",
        }
        for k, v in good_tests.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.nbq(), v)

        # This should return "0" - as the read is too small
        fake_read.return_value = "12"
        self.assertEqual(self.rig.nbq(), "0")

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_mode(self, fake_read):
        tc = namedtuple("tc", "mode read_data result")
        good_tests = [
            tc("L", "0010", "lsb"),
            tc("LSB", "0010", "lsb"),
            tc("U", "0020", "usb"),
            tc("usb", "0020", "usb"),
            tc("c", "0030", "cw"),
            tc("cw", "0030", "cw"),
            tc("CW", "0030", "cw"),
            tc("cwr", "0050", "cwr"),
            tc("CWR", "0050", "cwr"),
            tc("r", "0060", "rtty"),
            tc("rtty", "0060", "rtty"),
            tc("RTTY", "0060", "rtty"),
            tc("rttyr", "0090", "rttyr"),
            tc("RTTYr", "0090", "rttyr"),
        ]
        for t in good_tests:
            fake_read.return_value = t.read_data
            self.assertEqual(self.rig.mode(t.mode), t.result)

        bad_tests = [
            tc("L", "1", "????"),
            tc("LSB", "11", "????"),
            tc("U", "111", "????"),
        ]

        for t in good_tests:
            fake_read.return_value = t.read_data
            self.assertEqual(self.rig.mode(t.mode), t.result)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_modeq(self, fake_read):
        good_tests = {
            "0010": "lsb",
            "0020": "usb",
            "0030": "cw",
            "0050": "cwr",
            "0060": "rtty",
            "0090": "rttyr",
            "0080": "???",
            "ABCD": "unk",
        }
        for k, v in good_tests.items():
            fake_read.return_value = k  # Set the return value from the read
            self.assertEqual(self.rig.modeq(), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_paq(self, fake_read):
        good_tests = {"0000": "off", "12": "0", "PA1;": "on", "PA2;": "off"}
        for k, v in good_tests.items():
            # print(f"{k} {v}")
            fake_read.return_value = k  # Set the return value from the read
            self.assertEqual(self.rig.paq(), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_pa(self, fake_read):
        tc = namedtuple("tc", "set read_data result")
        good_data = [
            tc("on", "PA1;", "on"),
            tc("ON", "PA1;", "on"),
            tc("OFF", "PA2;", "off"),
            tc("off", "PA2;", "off"),
        ]
        for t in good_data:
            fake_read.return_value = t.read_data
            self.assertEqual(self.rig.pa(t.set), t.result)

        # Check that there is an error thrown for bad request
        self.assertRaises(ValueError, self.rig.pa, **{"pre_amp_setting": "maybe"})

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_power(self, fake_read):
        good_data = {
            "P20000": "20.0",
            "P30000": "30.0",
            "P65500": "65.5",
            "P99999": "99.9",
        }
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.power(int(float(v))), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_powerq(self, fake_read):

        good_data = {
            "P20000": "20.0",
            "P30000": "30.0",
            "P65500": "65.5",
            "P99999": "99.9",
            "P1": "0",
            "P11": "0",
            "P112": "0",
            "P113": "0",
            "P1144": "0",
            "PQRP": "0",
            "QRO": "0",
            "QROQRO": "??",
            "QRPQRP": "??",
        }
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.powerq(), v)

    # def test_vfoa(self):
    #     self.rig.vfoa()

    # def test_vfob(self):
    #     assert True
    #

    # todo vfoq is wrong.
    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_vfoq(self, fake_read):
        good_data = {
            "12345678": "Unk",
            "1": "0",
            "12": "0",
            "123": "0",
            "1234": "0",
            "12345": "0",
            "123456": "0",
            "1234567": "0",
        }
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.vfoq(), v)

    def test_sendcw_orig(self):
        self.assertIsNone(
            self.rig.sendcw("the;quick;brown;fox;jumped;over;the;lazy;dog")
        )

    def test_sendcw(self):
        self.assertIsNone(self.rig.sendcw("thequickbrownfoxjumpedoverthelazydog"))

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_cwspeedq(self, fake_read):

        good_data = {"K005;": 5, "K015;": 15, "K025;": 25, "K035;": 35, "K045;": 45}
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.cwspeedq(), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_cwspeed(self, fake_read):

        good_data = {"K005;": 5, "K015;": 15, "K025;": 25, "K035;": 35, "K045;": 45}
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.cwspeed(v), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_raq(self, fake_read):
        good_data = {"RA00;": "off", "RA01;": "on", "R;": "Unk"}

        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.raq(), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_ra(self, fake_read):
        tc = namedtuple("tc", "set read_data result")
        good_data = [tc(0, "RA00;", "off"), tc(1, "RA01;", "on")]
        for t in good_data:
            fake_read.return_value = t.read_data
            self.assertEqual(self.rig.ra(t.set), t.result)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_filter(self, fake_read):
        for n in range(0, 10):
            self.assertIsNone(self.rig.filter(n))

        # Make sure this raises an Exception
        self.assertRaises(ValueError, self.rig.filter, **{"n": 10})

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_filtern(self, fake_read):
        good_data = {
            "002400000": "0",
            "002412130": "1",
            "002412230": "2",
            "002412330": "3",
            "00": "0",
        }
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.filtern(), v)

    @patch("ham.equipment.elecraft.radio.K3.read")
    def test_filterq(self, fake_read):
        good_data = {
            "002400000": "2400Hz 0",
            "002412130": "2412Hz 3",
            "002412230": "2412Hz 3",
            "002412330": "2412Hz 3",
        }
        for k, v in good_data.items():
            fake_read.return_value = k
            self.assertEqual(self.rig.filterq(), v)

    def test_displayq(self):
        self.rig.displayq()

    # def test_verq(self):
    #     assert True
    #
    # def test_showtext(self):
    #     assert True
    #
    # def test_k3lcdchar(self):
    #     assert True
    #
    # def test_timeq(self):
    #     assert True
    #
    # def test_fixtime(self):
    #     assert True
    #
    # def test_set_channel(self):
    #     assert True
    #
    # def test_use_channel(self):
    #     assert True

    def test_end_to_end(self):
        print("testing K3")
        print("What Mode")
        print("" + self.rig.modeq())
        print("Check PreAmp")
        print("" + self.rig.paq())
        print("PreAmp on")
        print("" + self.rig.pa("on"))
        print("VFO-A")
        print("" + self.rig.qsyq())
        print("VFO-B")
        print("" + self.rig.qsyq2())
        print("FIQ")
        print("" + self.rig.fiq())
        print("Noise Blocker-A")
        print("" + self.rig.nbq())
        print("Mode")
        print("" + self.rig.modeq())
        print("Pre Amp")
        print("" + self.rig.paq())
        print("Power Settings")
        print("" + self.rig.powerq())
        print("VFO")
        print("" + self.rig.vfoq())
        print("CW Speed")
        print(f"{self.rig.cwspeedq()}")
        print("RA ")
        print("" + self.rig.raq())
        print("Filter")
        print(f"{self.rig.filterq()}")
        print("Display")
        print("" + self.rig.displayq())
        # print("Ver")
        # print('' + self.rig.verq(, x))
        print("Time")
        print("" + self.rig.timeq())
        print("Tests Finished")
