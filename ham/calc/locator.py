from __future__ import division
from datetime import datetime
from typing import Tuple, Dict
from math import sin, cos, atan2, sqrt, radians, degrees
import logging
import ephem
import pytz


class Locator(object):
    """
    Original code from pyham-utils
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("{} initialized")
        self.UTC = pytz.UTC

    @staticmethod
    def latlong_to_locator(latitude: float, longitude: float) -> str:

        """converts WGS84 coordinates into the corresponding Maidenhead Locator
            Args:
                latitude (float): Latitude
                longitude (float): Longitude
            Returns:
                string: Maidenhead locator

            Raises:
                ValueError: When called with wrong or invalid input args
                TypeError: When args are non float values

            Example:
               The following example converts latitude and longitude into the Maidenhead locator

               >>> from locator import latlong_to_locator
               >>> latitude = 48.5208333
               >>> longitude = 9.375
               >>> latlong_to_locator(latitude, longitude)
               'JN48QM'

            Note:
                 Latitude (negative = West, positive = East)
                 Longitude (negative = South, positive = North)

        """

        if longitude >= 180 or longitude <= -180:
            raise ValueError

        if latitude >= 90 or latitude <= -90:
            raise ValueError

        longitude += 180.0
        latitude += 90.0

        locator_str = chr(ord("A") + int(longitude / 20))
        locator_str += chr(ord("A") + int(latitude / 10))
        locator_str += chr(ord("0") + int((longitude % 20) / 2))
        locator_str += chr(ord("0") + int(latitude % 10))
        locator_str += chr(
            ord("A") + int((longitude - int(longitude / 2) * 2) / (2 / 24))
        )
        locator_str += chr(
            ord("A") + int((latitude - int(latitude / 1) * 1) / (1 / 24))
        )

        return locator_str

    @staticmethod
    def locator_to_latlong(locator_str) -> Tuple[float, float]:
        """
            converts Maidenhead locator in the corresponding WGS84 coordinates

            Args:
                locator_str (string): Locator, either 4 or 6 characters

            Returns:
                tuple (float, float): Latitude, Longitude

            Raises:
                ValueError: When called with wrong or invalid input arg
                TypeError: When arg is not a string

            Example:
               The following example converts a Maidenhead locator into Latitude and Longitude

               >>> from locator import locator_to_latlong
               >>> latitude, longitude = locator_to_latlong("JN48QM")
               >>> print latitude, longitude
               48.5208333333 9.375

            Note:
                 Latitude (negative = West, positive = East)
                 Longitude (negative = South, positive = North)

        """

        locator_str = locator_str.upper()

        if len(locator_str) == 5 or len(locator_str) < 4:
            raise ValueError

        if ord(locator_str[0]) > ord("R") or ord(locator_str[0]) < ord("A"):
            raise ValueError

        if ord(locator_str[1]) > ord("R") or ord(locator_str[1]) < ord("A"):
            raise ValueError

        if ord(locator_str[2]) > ord("9") or ord(locator_str[2]) < ord("0"):
            raise ValueError

        if ord(locator_str[3]) > ord("9") or ord(locator_str[3]) < ord("0"):
            raise ValueError

        if len(locator_str) == 6:
            if ord(locator_str[4]) > ord("X") or ord(locator_str[4]) < ord("A"):
                raise ValueError
            if ord(locator_str[5]) > ord("X") or ord(locator_str[5]) < ord("A"):
                raise ValueError

        longitude = (ord(locator_str[0]) - ord("A")) * 20 - 180
        latitude = (ord(locator_str[1]) - ord("A")) * 10 - 90
        longitude += (ord(locator_str[2]) - ord("0")) * 2
        latitude += ord(locator_str[3]) - ord("0")

        if len(locator_str) == 6:
            longitude += ((ord(locator_str[4])) - ord("A")) * (2 / 24)
            latitude += ((ord(locator_str[5])) - ord("A")) * (1 / 24)

            # move to center of sub-square
            longitude += 1 / 24
            latitude += 0.5 / 24

        else:
            # move to center of square
            longitude += 1
            latitude += 0.5

        return latitude, longitude

    def calculate_distance_km(self, locator1, locator2):
        """calculates the (shortpath) distance between two Maidenhead locators

            Args:
                locator1 (string): Locator, either 4 or 6 characters
                locator2 (string): Locator, either 4 or 6 characters

            Returns:
                float: Distance in km

            Raises:
                ValueError: When called with wrong or invalid input arg
                AttributeError: When args are not a string

            Example:
               The following calculates the distance between two Maidenhead locators in km

               >>> from pyhamtools.Locator import calculate_distance
               >>> calculate_distance("JN48QM", "QF67bf")
               16466.413

        """

        R = 6371  # earth radius in kms
        lat1, long1 = self.locator_to_latlong(locator1)
        lat2, long2 = self.locator_to_latlong(locator2)

        d_lat = radians(lat2) - radians(lat1)
        d_long = radians(long2) - radians(long1)

        r_lat1 = radians(lat1)
        # r_long1 = radians(long1)
        r_lat2 = radians(lat2)
        # r_long2 = radians(long2)

        a = sin(d_lat / 2) * sin(d_lat / 2) + cos(r_lat1) * cos(r_lat2) * sin(
            d_long / 2
        ) * sin(d_long / 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        d = R * c  # distance in km

        return d

    def calculate_distance_longpath(self, locator1, locator2):
        """calculates the (longpath) distance between two Maidenhead locators

            Args:
                locator1 (string): Locator, either 4 or 6 characters
                locator2 (string): Locator, either 4 or 6 characters

            Returns:
                float: Distance in km

            Raises:
                ValueError: When called with wrong or invalid input arg
                AttributeError: When args are not a string

            Example:
               The following calculates the longpath distance between two Maidenhead locators in km
                >>>
                >>> from locator import calculate_distance_longpath
                >>> calculate_distance_longpath("JN48QM", "QF67bf")
               23541.5867

        """

        c = 40008  # [km] earth circumference in kms
        sp = self.calculate_distance_km(locator1, locator2)

        return c - sp

    def calculate_heading(self, locator1: str, locator2: str) -> float:
        """calculates the heading from the first to the second locator

            Args:
                locator1 (string): Locator, either 4 or 6 characters
                locator2 (string): Locator, either 4 or 6 characters

            Returns:
                float: Heading in deg

            Raises:
                ValueError: When called with wrong or invalid input arg
                AttributeError: When args are not a string

            Example:
               The following calculates the heading from locator1 to locator2

               >>> from locator import calculate_heading
               >>> calculate_heading("JN48QM", "QF67bf")
               74.3136

        """

        lat1, long1 = self.locator_to_latlong(locator1)
        lat2, long2 = self.locator_to_latlong(locator2)

        r_lat1 = radians(lat1)
        r_lon1 = radians(long1)

        r_lat2 = radians(lat2)
        r_lon2 = radians(long2)

        d_lon = radians(long2 - long1)

        b = atan2(
            sin(d_lon) * cos(r_lat2),
            cos(r_lat1) * sin(r_lat2) - sin(r_lat1) * cos(r_lat2) * cos(d_lon),
        )  # Bearing calc
        bd = degrees(b)
        br, bn = divmod(bd + 360, 360)  # the Bearing remainder and final Bearing

        return bn

    def calculate_heading_longpath(self, locator1: str, locator2: str) -> float:
        """calculates the heading from the first to the second locator (long path)

            Args:
                locator1 (string): Locator, either 4 or 6 characters
                locator2 (string): Locator, either 4 or 6 characters

            Returns:
                float: Long path heading in deg

            Raises:
                ValueError: When called with wrong or invalid input arg
                AttributeError: When args are not a string

            Example:
               The following calculates the long path heading from locator1 to locator2

               >>> from locator import calculate_heading_longpath
               >>> calculate_heading_longpath("JN48QM", "QF67bf")
               254.3136

        """

        heading = self.calculate_heading(locator1, locator2)

        lp = (heading + 180) % 360

        return lp

    def calculate_sunrise_sunset(
        self, locator_str: str, calc_date: datetime = datetime.utcnow()
    ) -> Dict:
        """calculates the next sunset and sunrise for a Maidenhead locator at a give date & time

            Args:
                locator_str (string): Maidenhead Locator, either 4 or 6 characters
                calc_date (datetime, optional): Starting datetime for the calculations (UTC)

            Returns:
                dict: Containing datetimes for morning_dawn, sunrise, evening_dawn, sunset

            Raises:
                ValueError: When called with wrong or invalid input arg
                AttributeError: When args are not a string

            Example:
               The following calculates the next sunrise & sunset for JN48QM on the 1./Jan/2014

               >>> from locator import calculate_sunrise_sunset
               >>> from datetime import datetime
               >>> import pytz
               >>> UTC = pytz.UTC
               >>> myDate = datetime(year=2014, month=1, day=1, tzinfo=UTC)
               >>> calculate_sunrise_sunset("JN48QM", myDate)
               {
                   'morning_dawn': datetime.datetime(2014, 1, 1, 6, 36, 51, 710524, tzinfo=<UTC>),
                   'sunset': datetime.datetime(2014, 1, 1, 16, 15, 23, 31016, tzinfo=<UTC>),
                   'evening_dawn': datetime.datetime(2014, 1, 1, 15, 38, 8, 355315, tzinfo=<UTC>),
                   'sunrise': datetime.datetime(2014, 1, 1, 7, 14, 6, 162063, tzinfo=<UTC>)
               }
               :param locator_str:

        """
        morning_dawn = None
        sunrise = None
        evening_dawn = None
        sunset = None

        latitude, longitude = self.locator_to_latlong(locator_str)

        if type(calc_date) != datetime:
            raise ValueError

        sun = ephem.Sun()
        home = ephem.Observer()

        home.lat = str(latitude)
        home.long = str(longitude)
        home.date = calc_date

        sun.compute(home)

        try:
            nextrise = home.next_rising(sun)
            nextset = home.next_setting(sun)

            home.horizon = "-6"
            beg_twilight = home.next_rising(sun, use_center=True)
            end_twilight = home.next_setting(sun, use_center=True)

            morning_dawn = beg_twilight.datetime()
            sunrise = nextrise.datetime()

            evening_dawn = nextset.datetime()
            sunset = end_twilight.datetime()

        except ephem.AlwaysUpError as e:
            morning_dawn = None
            sunrise = None
            evening_dawn = None
            sunset = None
        except ephem.NeverUpError as e:
            morning_dawn = None
            sunrise = None
            evening_dawn = None
            sunset = None

        result = {
            "morning_dawn": morning_dawn,
            "sunrise": sunrise,
            "evening_dawn": evening_dawn,
            "sunset": sunset,
        }

        if morning_dawn:
            result["morning_dawn"] = morning_dawn.replace(tzinfo=self.UTC)
        if sunrise:
            result["sunrise"] = sunrise.replace(tzinfo=self.UTC)
        if evening_dawn:
            result["evening_dawn"] = evening_dawn.replace(tzinfo=self.UTC)
        if sunset:
            result["sunset"] = sunset.replace(tzinfo=self.UTC)
        return result
