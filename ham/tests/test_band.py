from unittest import TestCase

from ham.band import HamBand


class TestCalcLocator(TestCase):
    def setUp(self) -> None:
        self.test_band = HamBand()

    def test_contest(self):
        self.assertEqual(self.test_band.contest, [80, 40, 20, 15, 10])

    def test_khz_to_meters(self):
        self.assertEqual(self.test_band.khz_to_m(1850.3), 160)
        self.assertEqual(self.test_band.khz_to_m(3621.2), 80)
        self.assertEqual(self.test_band.khz_to_m(7021.2), 40)
        self.assertEqual(self.test_band.khz_to_m(10121.2), 30)
        self.assertEqual(self.test_band.khz_to_m(14021.2), 20)
        self.assertEqual(self.test_band.khz_to_m(18088.9999), 18)
        self.assertEqual(self.test_band.khz_to_m(21030.543), 15)
        self.assertEqual(self.test_band.khz_to_m(24895.1), 12)
        self.assertEqual(self.test_band.khz_to_m(28010.7), 10)

    def test_index(self):
        self.assertEqual(self.test_band.index(160), 0)
        self.assertEqual(self.test_band.index(80), 1)
        self.assertEqual(self.test_band.index(60), 2)
        self.assertEqual(self.test_band.index(40), 3)
        self.assertEqual(self.test_band.index(30), 4)
        self.assertEqual(self.test_band.index(20), 5)
        self.assertEqual(self.test_band.index(18), 6)
        self.assertEqual(self.test_band.index(15), 7)
        self.assertEqual(self.test_band.index(12), 8)
        self.assertEqual(self.test_band.index(10), 9)
