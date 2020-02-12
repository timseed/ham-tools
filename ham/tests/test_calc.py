from unittest import TestCase

from ham.calc import Locator, WindForce


class TestCalcLocator(TestCase):
    def setUp(self) -> None:
        """
        This runs before every test
        :return:
        """

        self.loc = Locator()


    def test_loc_manila(self):
        """
        Basic Lat Lon
        :return:
        """
        loc_str = self.loc.latlong_to_locator(15.0, 119.0)
        self.assertEqual(loc_str, "OK95MA")
        self.assertEqual(
            self.loc.locator_to_latlong(loc_str),
            (15.020833333333334, 119.04166666666667),
        )

    def test_loc_manila2(self):
        """
        Refined Lat Lon
        :return:
        """
        loc_str = self.loc.latlong_to_locator(15.1, 119.1)
        self.assertEqual(loc_str, "OK95NC")
        self.assertEqual(
            self.loc.locator_to_latlong(loc_str), (15.104166666666668, 119.125)
        )

    def test_loc_manila3(self):
        """
        Accurate Lat Lon (makes no difference)
        :return:
        """
        loc_str = self.loc.latlong_to_locator(15.1111, 119.11111)
        self.assertEqual(loc_str, "OK95NC")
        self.assertEqual(
            self.loc.locator_to_latlong(loc_str), (15.104166666666668, 119.125)
        )

    def test_bearing(self):
        """
        Check the Bearing and the distances
        :return:
        """
        mct_grid = self.loc.latlong_to_locator(23.3, 58.3)
        tele_grid = self.loc.latlong_to_locator(15.19, 120.78)
        dist = self.loc.calculate_distance_km(mct_grid, tele_grid)
        self.assertEqual(dist, 6576.247536801719)  # Note Kms
        short_path_bearing = self.loc.calculate_heading(mct_grid, tele_grid)
        long_path_bearing = self.loc.calculate_heading_longpath(mct_grid, tele_grid)
        self.assertEqual(short_path_bearing, 85.70847922042742)
        self.assertEqual(long_path_bearing, 265.7084792204274)


class TestWindForce(TestCase):
    def setUp(self) -> None:
        self.wf = WindForce()
        self.wind_in_mph = 50
        self.ant_size = 12.5  # TH11 !!

    def test_wf(self):
        wind_in_mph = 50
        ant_size = 12.5
        force = self.wf.generic(ant_size, wind_in_mph)  # TH11 Strong wind
        self.assertEqual(force, 960.0)

    def test_eia(self):
        force = self.wf.eia222f(self.ant_size, self.wind_in_mph)
        self.assertEqual(force, 991.0955373216017)

        # Increase the Height
        # Should be more Force
        force = self.wf.eia222f(self.ant_size, self.wind_in_mph, height_in_meters=20)
        self.assertEqual(force, 1161.7092867216038)

        # Make antenna "slippier"  - should be less force
        force = self.wf.eia222f(
            self.ant_size, self.wind_in_mph, drag=1.0, height_in_meters=20
        )
        self.assertEqual(force, 968.091072268003)
