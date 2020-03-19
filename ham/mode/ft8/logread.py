from dataclasses import dataclass
from datetime import datetime
from pprint import pprint
from ham.calc import Locator
from ham.band import HamBand
import pytz
from geojson import FeatureCollection, LineString
import json
from enum import Enum
import pickle

"""
Convert my WSJX Log file into Geo Json.
So I can use my own Python Server to render.

Suggested Useage

    lr = LogRead(""/Users/tim/Library/Application Support/WSJT-X/ALL_WSPR.TXT")
    lr.dump_geo_to_file()
    print("done")

This will output MySpots.json, please alter the input filename... to suit.
"""


class TOD(Enum):
    """
    Abstration of the Time of Day.
    """

    NIGHT = 1
    SUNRISE = 2
    MORNING = 3
    NOON = 4
    AFTERNOON = 5
    SUNSET = 6


class TimeOfDay:
    def calc_tod(self, date_time_dict, time_of_qso) -> str:
        """
        With 4 values in dictionary we should be able to determine when the TOD is.
        :param date_time_dict:
        :param time_of_qso:
        :return:
        """
        return str(TOD.SUNSET)


@dataclass
class ft8Qso:
    when: datetime
    timeofday: str
    band: int
    call: str
    grid: str
    lat: float = 0.0
    lon: float = 0.0
    heading_sp: float = 0.0
    distance_sp_km: float = 0.0

    @property
    def __geo_interface__(self):
        return str(
            {
                "type": "Feature",
                "properties": {
                    "name": self.call,
                    "band": self.band,
                    "popupContent": "{self.call} on {self.band}",
                },
                "geometry": {"type": "Point", "coordinates": [{self.lat}, {self.lon}]},
            }
        )


class LogRead:
    def __init__(
        self,
        my_qra: str = "PK05je",
        filename: str = "/Users/tim/Data/ft8.dat",
        tz="Asia/Manila",
    ):
        """
        Initialize the class.
        :param filename: Filename of the Log file
        :param tz: The Timezone of your location.
        """
        self.filename = filename
        self.my_qra = my_qra
        self.band = HamBand()
        self.tz = tz
        self.qso = []
        self.process()
        self.tod = TimeOfDay()

    def process(self):
        """
        My log file looks something like this ... We only
        Want lines with the QRA on them... the others are responding to other QSOs

        200221 000030  11.0  -3  0.18 14074352 JH7OTG        QM08
        200221 000030   7.5  -4  0.08 14075982 JA6BXA        PM52
        200221 000030   8.7  -5  0.00 18101824 BH4IGO
        200221 000045  11.5  -5  0.20 14074760 JA8ECS        QN03
        200221 000100   5.7  -5  0.20  7075672 BG5GLV        PL09
        200221 000115  12.2   0  0.00  7075745 YB5HPT        OI09
        200221 000115   5.6 -12 -0.62 10137410 JP3SHI
        200221 000130   9.8   1 -0.03  7074414 XV1X          OK33
        200221 000130   3.0  -8 -0.06  7075581 DV3CEP        PK05
        200221 000145   3.3  -7 -0.02  7076183 YF5TKN        OJ20
        200221 000215  14.3  -4 -0.05  7075135 YD4URY        OI25


        :return:
        """
        maidenhead = Locator()
        band = HamBand()
        with open(self.filename, "rt") as log_file:
            for line in log_file:
                parts = line.split()
                bearing_short_path = 0
                distance_short_path_km = 0.0
                if len(parts) == 8:
                    # Ignore the Tx Lines
                    try:
                        whn_noutc = datetime.strptime(
                            f"20{parts[0]}{parts[1]}", "%Y%m%d%H%M%S"
                        )
                        whn = whn_noutc.replace(tzinfo=pytz.UTC)
                        aprox_lat, aprox_lon = Locator.locator_to_latlong(
                            parts[7] + "LM"
                        )
                        bearing_short_path = maidenhead.calculate_heading(
                            self.my_qra, parts[7] + "LM"
                        )
                        distance_short_path_km = maidenhead.calculate_distance_km(
                            self.my_qra, parts[7] + "LM"
                        )

                        #
                        # Hack for Leaflet.js
                        # As I am close to the Pacific .... It plots Ph to US via Europe
                        # THis is called the " antimeridian artifacts"
                        # So if I have a longitude < -15 (Ireland, North Africa) I make it postive
                        if aprox_lon < -15.0:
                            aprox_lon += 360.0

                        self.qso.append(
                            ft8Qso(
                                when=whn,
                                # ToDO timeofday
                                timeofday="unk",
                                band=self.band.khz_to_m(float(parts[5]) / 1000.0),
                                call=parts[6],
                                grid=parts[7] + "LM",
                                lat=aprox_lat,
                                lon=aprox_lon,
                                heading_sp=bearing_short_path,
                                distance_sp_km=distance_short_path_km,
                            )
                        )
                    except ValueError as ve:
                        print(f"{str(ve)} problem with {parts[0]}{parts[1]}")

    def dump(self):
        pprint(self.qso)

    def dump_geo(self):
        my_lat, my_lon = Locator.locator_to_latlong(self.my_qra)
        return FeatureCollection(
            [
                LineString(
                    [(my_lon, my_lat), (q.lon, q.lat)],
                    properties={
                        "band": q.band,
                        "call": q.call,
                        "when": q.when.hour,
                        "distance": q.distance_sp_km,
                        "heading": q.heading_sp,
                    },
                )
                for q in self.qso
            ]
        )

    def dump_data(self):
        """
        Output data in a flat format for csv, pandas etc
        :return:
        """

        my_lat, my_lon = Locator.locator_to_latlong(self.my_qra)

        return [
            {
                "my_lat": my_lat,
                "my_lon": my_lon,
                "their_lat": q.lat,
                "their_lon": q.lon,
                "bearing": q.heading_sp,
                "distance": q.distance_sp_km,
                "band": q.band,
                "call": q.call,
                "when": q.when.hour,
            }
            for q in self.qso
        ]

    def dump_geojson_to_file(self, filename: str = "Myft8Spots.json"):
        with open(filename, "wt") as geoJsonFile:
            json.dump(self.dump_geo(), geoJsonFile)

    def dump_data_to_pickle(self, filename: str = "Myft8Spots.pkl"):
        with open(filename, "wb") as pickle_file:
            pickle.dump(self.dump_geo(), pickle_file)
