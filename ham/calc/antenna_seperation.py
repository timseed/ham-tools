"""source:http://www.antenna-theory.com/basics/friis.php

This theory is copyright... So the web page says.
"""


class AntSeperation:

    pi = 3.1415926
    safe_limit = 0.03  # Watts per sq/m

    def __init__(self, power=100, distance=10, txgain=1, rxgain=1):
        """

        :param power: Watts
        :param distance: Meters
        :param txgain: Gain of Tx i.e. 3 for 3 times input power. Not DB
        :param rxgain: ain of Rx i.e. 3 for 3 times. Not DB
        """
        self._power = power
        self._distance = distance
        self._txgain = txgain
        self._rxgain = rxgain

    def rx_power(self):
        """
        Calculate the amount of power the Rx antenna recieves
        """

        pwr = self._power * self._txgain * self._rxgain
        watts_per_meter = pwr / (4 * AntSeperation.pi * self._distance * self._distance)
        return watts_per_meter

    def is_safe_limit(self, watts_per_meter: float) -> str:
        """
        There seems to be many definitions of a safe limit.
        https://www.home-biology.com/electromagnetic-field-radiation-meters/safe-exposure-limits

        For example, the scientific group BioInitiative Working Group, which in our opinion is the most prestigious, now suggest a safety limit of 3-6 microwatts / m2 while in 2007 they proposed 100-1000 microwatts / m2.

        So I will assume that the day-time (i.e. not exposed in your sleep) limit is 0.01 Watts
        :return:
        """

        if watts_per_meter <= AntSeperation.safe_limit:
            return "Safe"
        else:
            return "Unsafe"
