import logging


class DxObj(object):
    """
    This hold the Dx Record of a Callsign allocation
    """

    def __init__(
        self,
        call_starts,
        country_name,
        cq_zone,
        itu_zone,
        continent_abbreviation,
        latitude,
        longitude,
        local_time_offset,
    ):
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
        self.logger = logging.getLogger(__name__)
        self._version = "1.0.1"

    def show(self):
        print(f"{self.dump()}")

    @property
    def Version(self):
        return self._version

    def __eq__(self, other):
        """
        Custom __eq__ this allows Python to compute
            assert obj == obj2
        Otherwise it fails and we have to check like
            if obj.Field == obj2.Field

        :param other:
        :return:
        """
        return (
            isinstance(other, DxObj)
            and self.Call_Starts == other.Call_Starts
            and self.Country_Name == other.Country_Name
            and self.Longitude == other.Longitude
            and self.Latitude == other.Latitude
            and self.ITU_Zone == other.ITU_Zone
            and self.CQ_Zone == other.CQ_Zone
        )

    def __repr__(self):
        """
        The official representation of this class
        :return:
        """
        return self.dump()

    def dump(self):
        return str.format(
            f"DxObj(call_starts='{self.Call_Starts}',country_name='{self.Country_Name}',cq_zone={self.CQ_Zone},itu_zone={self.ITU_Zone},"
            f"continent_abbreviation='{self.Continent_Abbreviation}',latitude={self.Latitude},"
            f"longitude={self.Longitude},local_time_offset={self.Local_time_offset})"
        )

    @property
    def Country_Name(self):
        return self._Country_Name

    @property
    def CQ_Zone(self):
        return self._CQ_Zone

    @property
    def ITU_Zone(self):
        return self._ITU_Zone

    @property
    def Continent_Abbreviation(self):
        return self._continent_abbreviation

    @property
    def Latitude(self):
        return self._Latitude

    @property
    def Longitude(self):
        return self._Longitude

    @property
    def Local_time_offset(self):
        return self._Local_time_offset

    @property
    def Call_Starts(self):
        return self._Call_Starts
