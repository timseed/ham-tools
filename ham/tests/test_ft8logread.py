from unittest import TestCase
from ham.mode.ft8 import LogRead


class test_ft8LogRead(TestCase):
    def setUp(self) -> None:
        self.mode = LogRead()

    def test_is_object(self):
        self.assertIsInstance(self.mode, LogRead)

    def test_process(self):
        assert True

    def test_dump(self):
        assert True

    def test_dump_geo(self):
        assert True

    def test_dump_geo_to_file(self):
        assert True
