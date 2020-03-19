from unittest import TestCase
from ham.calc import Locator
from ham.dxcc import DxObj, DxccAll


class TestDxccAll(TestCase):
    def setUp(self):
        self.dxcc = DxObj("A4", "Oman", 23, 13, "As", 21.1, 58.2, 4.0)
        self.loc = Locator()
        self.assertTrue(self.dxcc)

    def test_continent(self):
        self.assertEqual(self.dxcc.Continent_Abbreviation, "As")

    def test_name(self):
        self.assertEqual(self.dxcc.Country_Name, "Oman")

    def test_cq_zone(self):
        self.assertEqual(self.dxcc.CQ_Zone, 23)

    def test_itu_zone(self):
        self.assertEqual(self.dxcc.ITU_Zone, 13)

    def test_lat(self):
        self.assertEqual(self.dxcc.Latitude, 21.1)

    def test_lon(self):
        self.assertEqual(self.dxcc.Longitude, 58.2)

    def test_timeoffset(self):
        self.assertEqual(self.dxcc.Local_time_offset, 4.0)

    def test_dxcc_list(self):
        b = DxccAll()
        manila = b.find("DU1ABC")
        manila_loc = self.loc.latlong_to_locator(manila.Latitude, manila.Longitude)
        for ctry in ["A9", "G", "KH6", "JA", "K", "VR2"]:
            tmp_ctry = b.find(ctry)
            tmp_locator = self.loc.latlong_to_locator(
                tmp_ctry.Latitude, tmp_ctry.Longitude
            )

            distance = self.loc.calculate_distance_km(manila_loc, tmp_locator)
            print(str.format("From DU to {} is {:6.1f} kms", ctry, distance))

        def check(self):
            b = self.dx_list.prefix
            for c in b:
                if c.startswith("A"):
                    print("" + c)
            junk = 1

    # def test_removewae(self):
    #     self.fail()
    #
    # def test_correctdata(self):
    #     self.fail()
    #
    # def test_read(self):
    #     self.fail()
    #
    # def test_show(self):
    #     self.fail()
    #
    # def test_showall(self):
    #     self.fail()
    #
    # def test_std_call(self):
    #     self.fail()
    #
    # def test_find(self):
    #     self.fail()
