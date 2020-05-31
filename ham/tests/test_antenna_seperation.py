from unittest import TestCase
from ham.calc import AntSeperation


class test_ant_deperation(TestCase):
    def setUp(self) -> None:
        self.ant_sep = AntSeperation()

    def test_is_class(self):
        self.assertIsInstance(self.ant_sep, AntSeperation)

    def test_std(self):
        self.assertEqual(self.ant_sep.rx_power(), 0.07957747290339301)

    def test_is_safe_limit(self):
        self.assertEqual(self.ant_sep.is_safe_limit(0.031), "Unsafe")
        self.assertEqual(self.ant_sep.is_safe_limit(0.03), "Safe")
        self.assertEqual(self.ant_sep.is_safe_limit(0.02999), "Safe")
