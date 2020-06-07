import daiquiri
import re
from ham.cabrillo.cabrillodata import Cabrillio


class Cab2Csv:
    def __init__(self):
        self.logger = daiquiri.getLogger(__name__)
        self.logger.debug("Cav2CSV init")
        self.re_line = re.compile(r"^QSO:")

    def read_cab(self, cab_file: str) -> str:
        lines = None
        with open(cab_file, "rt") as ifp:
            lines = ifp.read()
        return lines

    def produce_qso(self, cab_lines):

        """
         --------info sent------- -------info rcvd--------
        QSO:  freq mo date       time call          rst exch   call          rst exch   t
        QSO: ***** ** yyyy-mm-dd nnnn ************* nnn ****** ************* nnn ****** n
        QSO:  3799 PH 1999-03-06 0711 HC8N           59 700    W1AW           59 CT     0
        QSO:  3799 PH 1999-03-06 0712 HC8N           59 700    N5KO
        """
        lines = []

        for n in cab_lines.split("\n"):
            if self.re_line.match(n):
                # Rip the "QSO: " from the front of the line.
                n = n[5:]
                data = dict(zip(Cabrillio.fields(),n.split(' ')))
                qso = Cabrillio(**data)
                lines.append(qso)
        return lines

    def to_adif(self,qsos:list)->str:
        lines=""
        for qso in qsos:
            line=""
            d=qso.as_dict()
            for f in Cabrillio.fields():
                line += f"<{f}:{len(d[f])}>{d[f]} >"
            if line:
                line += " <EOR>\n"
                lines += line
        return lines




