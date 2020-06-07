from unittest import TestCase
from unittest.mock import patch, mock_open
from ham.cabrillo import Cab2Csv, Cabrillio

cab_text="""START-OF-LOG: 3.0
CALLSIGN: A45WG
CONTEST: DARC-WAEDC-SSB
CATEGORY: SINGLE-OP HIGH
CATEGORY-BAND: ALL
CLAIMED-SCORE: 13720
CLUB: 
LOCATION: Muscat, Oman
CREATED-BY: RUMlogNG (3.7.1) by DL2RUM
EMAIL: tim@sy-edm.com
NAME: Tim Seed
ADDRESS: PO Box 2260
ADDRESS: Ruwi 
ADDRESS: Pc 112
ADDRESS: Sultante of Oman
OPERATORS: a45WG
SOAPBOX: Difficult conditions to say the least.
QSO: 14000 PH 2017-09-09 0508 A45WG         599 001    UA7K          599 112    0
QSO: 14000 PH 2017-09-09 0510 A45WG         599 002    DF0HQ         599 076    0
QSO: 14000 PH 2017-09-09 0511 A45WG         599 003    DL5L          599 45     0
QSO: 14000 PH 2017-09-09 0511 A45WG         599 004    TM5N          599 75     0
QSO: 14000 PH 2017-09-09 0512 A45WG         599 005    DK0RX         599 035    0
QSO: 14000 PH 2017-09-09 0513 A45WG         599 006    RN4HAB        599 006    0
QSO: 14000 PH 2017-09-09 0514 A45WG         599 007    UZ2I          599 25     0
QSO: 14268 PH 2017-09-09 1704 A45WG         59  008    F4EPM         59  14     0
QSO: 14268 PH 2017-09-09 1705 A45WG         59  009    DF9VJ         59  080    0
QSO: 14297 PH 2017-09-09 1711 A45WG         59  010    F6BLZ         59  84     0
QSO: 14297 PH 2017-09-09 1712 A45WG         59  011    YO4BEX        59  019    0
QSO: 14297 PH 2017-09-09 1713 A45WG         59  012    DL6RAI        59  035    0
QSO: 14297 PH 2017-09-09 1715 A45WG         59  013    9A5O          59  026    0
END-OF-LOG:
"""

expected_adif = """<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0508 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0510 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0511 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0511 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0512 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0513 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14000 ><mode:2>PH ><date:10>2017-09-09 ><time:4>0514 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14268 ><mode:2>PH ><date:10>2017-09-09 ><time:4>1704 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14268 ><mode:2>PH ><date:10>2017-09-09 ><time:4>1705 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14297 ><mode:2>PH ><date:10>2017-09-09 ><time:4>1711 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14297 ><mode:2>PH ><date:10>2017-09-09 ><time:4>1712 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14297 ><mode:2>PH ><date:10>2017-09-09 ><time:4>1713 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR>
<freq:5>14297 ><mode:2>PH ><date:10>2017-09-09 ><time:4>1715 ><my_call:5>A45WG ><rst:0> ><exch:0> ><their_call:0> > <EOR> != 123
"""

class test_cab2csv(TestCase):


    def setUp(self) -> None:
        self.cab = Cab2Csv()

    def test_is_instance(self):
        self.assertIsInstance(self.cab, Cab2Csv)

    @patch('builtins.open', mock_open(read_data=cab_text))
    def test_read_cab(self):
        rv=self.cab.read_cab('/dev/null')
        self.assertEqual(rv,cab_text)

    @patch('builtins.open', mock_open(read_data=cab_text))
    def test_produce_qso(self):
        all_lines=self.cab.read_cab('/dev/null')
        qsos = self.cab.produce_qso(all_lines)
        self.assertEqual(13,len(qsos))

    @patch('builtins.open', mock_open(read_data=cab_text))
    def test_produce_qso(self):
        all_lines=self.cab.read_cab('/dev/null')
        qsos = self.cab.produce_qso(all_lines)
        self.assertEqual(13,len(qsos))
        self.assertIsInstance(qsos[0],Cabrillio)
        adif_text=self.cab.to_adif(qsos)
        self.assertEqual(expected_adif[:500],adif_text[:500])

