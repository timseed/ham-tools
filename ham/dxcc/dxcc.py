"""

"""
class DxCc(object):
    """

    """
    def __init__(self, call_starts: str, country_name: str, cq_zone: int, itu_zone: int, continent_abbreviation: str,
                 latitude: float, longitude: float,
                 local_time_offset: float):
        """
        Create a Country - note this is using the CallSign Prefix
        :param call_starts:
        param Country_Name:
        :param cq_zone:
        :param itu_zone:
        :param continent_abbreviation:
        :param latitude:
        :param longitude:
        :param local_time_offset:
        :return:
        """
        self._Call_Starts = call_starts
        self._Country_Name = country_name
        self._CQ_Zone = cq_zone
        self._ITU_Zone = itu_zone
        self._continent_abbreviation = continent_abbreviation
        self._Latitude = latitude
        self._Longitude = longitude
        self._Local_time_offset = local_time_offset

    def show(self) -> None:
        print(
            str.format('Country {}:\n\tCQ\t{}\n\tITU\t{}\n\tAbbv\t{}\n\t\tPos\n\t\t\tLat\t{}\n\t\t\tLon\t{}\n\tTZ\t{}',
                       self._Country_Name,
                       self._CQ_Zone,
                       self._ITU_Zone,
                       self._continent_abbreviation,
                       self._Latitude,
                       self._Longitude,
                       self._Local_time_offset
                       ))

    @property
    def country_name(self) -> str:
        return self._Country_Name

    @property
    def cq_zone(self) -> int:
        return self._CQ_Zone

    @property
    def itu_zone(self) -> int:
        return self._ITU_Zone

    @property
    def continent_abbreviation(self) -> str:
        return self._continent_abbreviation

    @property
    def latitude(self) -> float:
        return self._Latitude

    @property
    def longitude(self) -> float:
        return self._Longitude

    @property
    def local_time_offset(self) -> float:
        return self._Local_time_offset
