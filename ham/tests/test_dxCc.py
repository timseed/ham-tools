from unittest import TestCase
from ham.dxcc import DxCc

class TestDxccAll(TestCase):

    def setUp(self) -> DxCc:
        self.dxcc = DxCc("A4", "Oman", 23, 13, "As",21.1, 58.2,4.0)
        self.assertTrue(self.dxcc)

    def test_continent(self):
        self.assertEqual (self.dxcc.continent_abbreviation,"As")

    def test_name(self):
        self.assertEqual (self.dxcc.country_name,"Oman")

    def test_cq_zone(self):
        self.assertEqual (self.dxcc.cq_zone,23)

    def test_itu_zone(self):
        self.assertEqual (self.dxcc.itu_zone,13)

    def test_lat(self):
        self.assertEqual(self.dxcc.latitude, 21.1)

    def test_lon(self):
        self.assertEqual(self.dxcc.longitude, 58.2)

    def test_timeoffset(self):
        self.assertEqual(self.dxcc.local_time_offset, 4.0)

    def test_show(self):
        self.assertEqual(self.dxcc.show("A45WG"),1 )


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
