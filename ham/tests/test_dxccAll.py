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

    #def test_show(self):
    #    self.assertEqual(self.dxcc_all.show("A45wg"), None)

    #def test_showall(self):
    #    self.assertIsInstance(self.dxcc_all.showall(), None)

    def test_std_call(self):
        self.assertEqual(self.dxcc_all.std_call("M0FGC/du3"), None)
        self.assertEqual(self.dxcc_all.std_call("du3/M0FGC"), None)
        self.assertEqual(self.dxcc_all.std_call("M0FGC"), "M0FGC")

    def test_find(self):
        self.assertIsNotNone(self.dxcc_all.find("A45WG"))
        self.assertIsNotNone(self.dxcc_all.find("DU3TIM"))
        self.assertIsNotNone(self.dxcc_all.find("DU3TIM"))
