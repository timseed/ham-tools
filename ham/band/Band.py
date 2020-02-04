import logging


class HamBand(object):
    """
    Convert from Khz to Meters in Ham Speak terms not literally
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.Band = [160, 80, 60, 40, 30, 20, 18, 15, 12, 10]
        self.ContestBand = [80, 40, 20, 15, 10]
        self.Freq = [
            (1800, 2000),
            (3500, 4000),
            (5000, 5100),
            (7000, 7300),
            (10100, 10150),
            (14000, 14350),
            (18068, 18168),
            (21000, 21450),
            (24890, 24990),
            (2800, 29700),
        ]
        self._band_plan = list(zip(self.Band, self.Freq))

    def khz_to_m(self, khz: float) -> int:
        """
        Convert Khz to Meters
        :return: String in Meters
        """

        khz = float(khz)
        khz = int(khz)

        rv = None
        for b in self._band_plan:
            if b[1][0] <= khz <= b[1][1]:
                rv = b[0]
                break
        return rv

    def index(self, band_in_meters: int) -> int:
        "Return the INDEX of the Band"
        if band_in_meters in self.Band:
            return self.Band.index(band_in_meters)
        else:
            return -1

    @property
    def contest(self) -> list:
        return self.ContestBand
