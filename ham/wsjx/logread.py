from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from ham.calc import Locator
from ham.band import HamBand
from geojson import Feature, Point, FeatureCollection, LineString
import json

"""
Convert my WSJX Log file into Geo Json.
So I can use my own Python Server to render.

Suggested Useage

    lr = LogRead(""/Users/tim/Library/Application Support/WSJT-X/ALL_WSPR.TXT")
    lr.dump_geo_to_file()
    print("done")
    
This will output MySpots.json, please alter the input filename... to suit.
"""


@dataclass
class WsjXQso:
    when: datetime
    band: int
    call: str
    grid: str
    lat: float = 0.0
    lon: float = 0.0

    @property
    def __geo_interface__(self):

        return str({
            'type': 'Feature',
            'properties': {
                'name': self.call,
                'band': self.band,
                'popupContent': '{self.call} on {self.band}',
            },
            'geometry': {'type': 'Point', 'coordinates': [{self.lat}, {self.lon}]},
        })


class LogRead:
    def __init__(
        self,
        my_qra: str = "PK05je",
        filename: str = "/Users/tim/Library/Application Support/WSJT-X/ALL_WSPR.TXT",
    ):
        """
        Initialize the class.
        :param filename: Filename of the Log file
        """
        self.filename = filename
        self.my_qra = my_qra
        self.qso = []
        self.process()

    def process(self):
        """
        My log file looks something like this ...

        200210_002000    18.105 Tx WSPR     0  0.0 1547 <DU3/M0FGC> PK04LO 37
        200210_002000    18.105 Tx WSPR     0  0.0 1547 <DU3/M0FGC> PK04LO 37
        200210 0024   3 -22  0.24  18.1060640  KR6LA CN90 37          -3     2    0    1  379  0
        200210 0024   2 -25  0.11  18.1061200  VK2JFP QF58 23          1     4    0    1   38  0
        200210 0024   2 -23 -0.74  18.1061936  VK4EKA QG62 30          0     4    0    1  200  0
        200210 0028   2 -26 -0.70  18.1061938  VK4EKA QG62 30          0    10    0    1   10  0
        200212 0336   2 -23  0.37  14.0971782  VK3GYH QF21 40          0     3    0    1  105  0
        200212 0340   4 -14 -0.27  14.0970291  P29ZL QI23 33           0     1    0    1  435  0
        200212 0340   3 -23 -4.07  14.0970701  BH1NSN OM89 23          0     1    0    1  334  0
        200212 0342   2 -27  0.15  14.0971009  BI1EIH ON80 27          0     6    0    1  -30  0
        :return:
        """
        maidenhead = Locator()
        band = HamBand()
        with open(self.filename, "rt") as log_file:
            for line in log_file:
                parts = line.split()
                if len(parts) == 15:
                    # Ignore the Tx Lines
                    try:
                        whn = datetime.strptime(f"20{parts[0]}{parts[1]}", "%Y%m%d%H%M")
                        aprox_lat, aprox_lon = Locator.locator_to_latlong(
                            parts[7] + "LM"
                        )
                        self.qso.append(
                            WsjXQso(
                                when=whn,
                                band=band.khz_to_m(1000.0 * float(parts[5])),
                                call=parts[6],
                                grid=parts[7] + "LM",
                                lat=aprox_lat,
                                lon=aprox_lon,
                            )
                        )
                    except ValueError as ve:
                        print(f"{str(ve)} problem with {parts[0]}{parts[1]}")

    def dump(self):
        pprint(self.qso)

    def dump_geo(self):
        my_lat, my_lon = Locator.locator_to_latlong(self.my_qra)
        return FeatureCollection([LineString([(my_lon, my_lat),(q.lon, q.lat)],
                                             properties={'band':q.band}) for q in self.qso])

    def dump_geo_to_file(self, filename: str = "MySpots.json"):
        with open(filename, "wt") as geoJsonFile:
            json.dump(lr.dump_geo(), geoJsonFile)


if __name__ == "__main__":
    lr = LogRead(my_qra='PK05je')
    lr.dump_geo_to_file()
    print("done")
