from unittest import TestCase
from ham.dxcc import DxccAll


class TestDxccAll(TestCase):
    def setUp(self) -> None:
        self.dxcc_all = DxccAll()

    def test_init_ok(self):
        self.assertTrue(self.dxcc_all)

    def test_removewae(self):
        self.assertTrue(self.dxcc_all.removewae())

    def test_correctdata(self):
        self.assertEqual(self.dxcc_all.correctdata("A4", "YG0[54]"), ("A4", "YG0[54]"))
        self.assertEqual(
            self.dxcc_all.correctdata("AA4", "YG0[54]"), ("AA4", "YG0[54]")
        )
        self.assertEqual(self.dxcc_all.correctdata("A4", "YG0(54)"), ("A4", "YG0(54)"))
        self.assertEqual(self.dxcc_all.correctdata("A4", "YG0{54}"), ("A4", "YG0{54}"))

    def test_read(self):
        self.assertGreater(self.dxcc_all.read(), 400)

    # def test_show(self):
    #    self.assertEqual(self.dxcc_all.show("A45wg"), None)

    # def test_showall(self):
    #    self.assertIsInstance(self.dxcc_all.showall(), None)

    def test_std_call(self):
        self.assertEqual(self.dxcc_all.std_call("M0FGC/du3"), None)
        self.assertEqual(self.dxcc_all.std_call("du3/M0FGC"), None)
        self.assertEqual(self.dxcc_all.std_call("M0FGC"), "M0FGC")

    def test_find(self):
        self.assertIsNotNone(self.dxcc_all.find("A45WG"))
        self.assertIsNotNone(self.dxcc_all.find("DU3TIM"))
        self.assertIsNotNone(self.dxcc_all.find("M0FGC"))

    def test_country_name(self):
        self.assertEqual(self.dxcc_all.find("M0FGC").Country_Name, "England")
        self.assertEqual(self.dxcc_all.find("GM0FGC").Country_Name, "Scotland")
        self.assertEqual(self.dxcc_all.find("DU20FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU1FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU1FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU3FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU4FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU5FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU6FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU7FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU8FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("DU9FGC").Country_Name, "Philippines")
        self.assertEqual(self.dxcc_all.find("F0FGC").Country_Name, "France")
        self.assertEqual(self.dxcc_all.find("JA1BOB").Country_Name, "Japan")
        self.assertEqual(self.dxcc_all.find("BD1CNY").Country_Name, "China")
        self.assertEqual(self.dxcc_all.find("K1BOB").Country_Name, "United States")
        self.assertEqual(self.dxcc_all.find("K2BOB").Country_Name, "United States")
        self.assertEqual(self.dxcc_all.find("K3BOB").Country_Name, "United States")
        self.assertEqual(self.dxcc_all.find("K4BOB").Country_Name, "United States")
        self.assertEqual(self.dxcc_all.find("K5BOB").Country_Name, "United States")
        self.assertEqual(self.dxcc_all.find("KH6BOB").Country_Name, "Hawaii")
        self.assertEqual(self.dxcc_all.find("LU2BOB").Country_Name, "Argentina")

    def test_continent(self):
        self.assertEqual(self.dxcc_all.find("M0FGC").Continent_Abbreviation, "EU")
        self.assertEqual(self.dxcc_all.find("GM0FGC").Continent_Abbreviation, "EU")
        self.assertEqual(self.dxcc_all.find("DU20FGC").Continent_Abbreviation,"OC")
        self.assertEqual(self.dxcc_all.find("DU1FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU1FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU3FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU4FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU5FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU6FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU7FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU8FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("DU9FGC").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("F0FGC").Continent_Abbreviation, "EU")
        self.assertEqual(self.dxcc_all.find("JA1BOB").Continent_Abbreviation, "AS")
        self.assertEqual(self.dxcc_all.find("BD1CNY").Continent_Abbreviation, "AS")
        self.assertEqual(self.dxcc_all.find("K1BOB").Continent_Abbreviation, "NA")
        self.assertEqual(self.dxcc_all.find("K2BOB").Continent_Abbreviation, "NA")
        self.assertEqual(self.dxcc_all.find("K3BOB").Continent_Abbreviation, "NA")
        self.assertEqual(self.dxcc_all.find("K4BOB").Continent_Abbreviation, "NA")
        self.assertEqual(self.dxcc_all.find("K5BOB").Continent_Abbreviation, "NA")
        self.assertEqual(self.dxcc_all.find("KH6BOB").Continent_Abbreviation, "OC")
        self.assertEqual(self.dxcc_all.find("LU2BOB").Continent_Abbreviation, "SA")