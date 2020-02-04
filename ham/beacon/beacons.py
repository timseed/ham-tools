import datetime
import logging
import sys
import time
from enum import Enum

__author__ = "timseed"


class BeaconFld(Enum):
    call, location, freq = range(3)


class Beacon(object):
    freq = [14.1, 18.11, 21.15, 24.930, 28.2]  # in Mhz

    def __init__(self, call, country, b14, b18, b21, b24, b28, owner, status):
        self.CALL = call
        self.Country = country
        self.band_time = []
        self.band_time.append(Beacon.time_str_to_secs(b14))
        self.band_time.append(Beacon.time_str_to_secs(b18))
        self.band_time.append(Beacon.time_str_to_secs(b21))
        self.band_time.append(Beacon.time_str_to_secs(b24))
        self.band_time.append(Beacon.time_str_to_secs(b28))
        self.owner = owner
        self.status = status
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def time_str_to_secs(tstr: str) -> int:

        """
        Replace Time_Str to seconds
        :param tstr:  In format of Min:Secs
        :return: int time_in_seconds
        """
        try:
            minute, sec = tstr.split(":")
            return int(minute) * 60 + int(sec)
        except ValueError:
            return -1


class Beacons(object):
    # Some Signals we want to send from this class
    freq = [14.1, 18.11, 21.15, 24.930, 28.2]  # in Mhz
    ref_datetime = datetime.datetime(2016, 1, 1, 0, 0, 1)

    def __init__(self, screenoutput=False):
        self.logger = logging.getLogger(__name__)
        self.bands = [14, 18, 21, 24, 28]  # in Mhz
        self.selected_band = -1  # Means ALL BANDS
        self.beacons = []
        self.ScreenOutput = screenoutput
        # Setup the Beacon Definitions
        self.beacons.append(
            Beacon(
                "U1UN",
                "United Nations",
                "00:00",
                "00:10",
                "00:20",
                "00:30",
                "00:40",
                "UNRC",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "VE8AT",
                "Canada",
                "00:10",
                "00:20",
                "00:30",
                "00:40",
                "00:50",
                "RAC/NARC",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "W6WX",
                "United States",
                "00:20",
                "00:30",
                "00:40",
                "00:50",
                "01:00",
                "NCDXF",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "KH6RS",
                "Hawaii",
                "00:30",
                "00:40",
                "00:50",
                "01:00",
                "01:10",
                "Maui ARC",
                "OFF9",
            )
        )
        self.beacons.append(
            Beacon(
                "ZL6B",
                "New Zealand",
                "00:40",
                "00:50",
                "01:00",
                "01:10",
                "01:20",
                "NZART",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "VK6RBP",
                "Australia",
                "00:50",
                "01:00",
                "01:10",
                "01:20",
                "01:30",
                "WIA",
                "OFF4",
            )
        )
        self.beacons.append(
            Beacon(
                "JA2IGY",
                "Japan",
                "01:00",
                "01:10",
                "01:20",
                "01:30",
                "01:40",
                "JARL",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "RR9O",
                "Russia",
                "01:10",
                "01:20",
                "01:30",
                "01:40",
                "01:50",
                "SRR",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "VR2B",
                "Hong Kong",
                "01:20",
                "01:30",
                "01:40",
                "01:50",
                "02:00",
                "HARTS",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "4S7B",
                "Sri Lanka",
                "01:30",
                "01:40",
                "01:50",
                "02:00",
                "02:10",
                "RSSL",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "ZS6DN",
                "South Africa",
                "01:40",
                "01:50",
                "02:00",
                "02:10",
                "02:20",
                "ZS6DN",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "5Z4B",
                "Kenya",
                "01:50",
                "02:00",
                "02:10",
                "02:20",
                "02:30",
                "ARSK",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "4X6TU",
                "Israel",
                "02:00",
                "02:10",
                "02:20",
                "02:30",
                "02:40",
                "IARC",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "OH2B",
                "Finland",
                "02:10",
                "02:20",
                "02:30",
                "02:40",
                "02:50",
                "SRAL",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "CS3B",
                "Madeira",
                "02:20",
                "02:30",
                "02:40",
                "02:50",
                "00:00",
                "ARRM",
                "OFF4",
            )
        )
        self.beacons.append(
            Beacon(
                "LU4AA",
                "Argentina",
                "02:30",
                "02:40",
                "02:50",
                "00:00",
                "00:10",
                "RCA",
                "OK",
            )
        )
        self.beacons.append(
            Beacon(
                "OA4B", "Peru", "02:40", "02:50", "00:00", "00:10", "00:20", "RCP", "OK"
            )
        )
        self.beacons.append(
            Beacon(
                "YV5B",
                "Venezuela",
                "02:50",
                "00:00",
                "00:10",
                "00:20",
                "00:30",
                "RCV",
                "OK",
            )
        )
        self.logger.info("Beacon class initialized")

    def SetBand(self, band: int) -> None:
        if band in self.bands:
            self.selected_band = self.bands.index(band)
            self.logger.info(str.format("Band changed to {}", band))
            self.logger.info(
                str.format("Freq to Listen is {}", self.freq[self.selected_band])
            )
            if self.ScreenOutput:
                print("" + (str.format("Band changed to {}", band)))
                print(
                    ""
                    + (
                        str.format(
                            "Freq to Listen is {}", self.freq[self.selected_band]
                        )
                    )
                )
        else:
            self.logger.error(str.format("Bad Band requested {}", band))

    def getdelay(self) -> tuple:
        tnow: datetime = datetime.datetime.now()
        delay: float = 10.0 - tnow.timestamp() % 10
        self.logger.info(str.format("tnow {}   delay {}", tnow, delay))
        return tnow, delay

    def minsec(self, offset: int) -> tuple:
        """
        Return Minute and Seconds offset of Timeslice
        :param offset:
        :return: Tuple (Min,Sec)
        """
        minutes: int = int(offset / 60)
        seconds: int = offset - (minutes * 60)
        return seconds, seconds

    def getstation(self) -> list:
        ts_now = datetime.datetime.now()
        time_diff = (Beacons.ref_datetime - ts_now).seconds
        next_beacon = ("Unk", "Unk")
        second_in_phase = ts_now.timestamp() % 180
        self.logger.info("Seconds in Phase = %d" % second_in_phase)
        next_active = (((int(second_in_phase / 10)) * 10) + 0) % 180
        OSet = self.minsec(next_active)
        self.logger.info(
            "Next Active %d in secs is %d Min %d " % (next_active, OSet[0], OSet[1])
        )

        self.logger.info(
            str.format(
                "Band {} Seconds {} next {} ",
                self.selected_band,
                second_in_phase,
                next_active,
            )
        )
        next_station = []
        if self.selected_band != -1:
            for b in self.beacons:
                if (
                    self.selected_band != -1
                    and b.band_time[self.selected_band] == next_active
                ):
                    self.logger.info(
                        str.format(
                            "Band time Index {}  {}",
                            b.CALL,
                            b.band_time[self.selected_band],
                        )
                    )
                    next_beacon = (b.CALL, b.Country, Beacon.freq[self.selected_band])
                    next_station.append(next_beacon)
                    # We are in Single Band Mode - find one and quit this loop
                    break
        else:
            for band in range(5):
                for b in self.beacons:
                    if b.band_time[band] == next_active:
                        next_beacon = (b.CALL, b.Country, Beacon.freq[band])
                        next_station.append(next_beacon)
                        break

        return next_station

    def beacon_start(self, timeout: int = 30) -> None:
        tnow, delay = self.getdelay()
        self.logger.info(str.format("timenow is {}", tnow.timestamp()))
        self.logger.info(str.format("delay   is {}", delay))
        while timeout > 0:
            timeout = timeout - delay
            next_station = self.getstation()  # Returns an Array of Stations
            self.logger.info("--------------")
            for ns in next_station:
                self.logger.info(
                    str.format(
                        "Call {:10s} Country {:30s} Freq {:7.2f}",
                        ns[BeaconFld.call.value],
                        ns[BeaconFld.location.value],
                        ns[BeaconFld.freq.value],
                    )
                )
                if self.ScreenOutput:
                    print(
                        ""
                        + str.format(
                            "Call {:10s} Country {:30s} Freq {:7.2f}",
                            ns[BeaconFld.call.value],
                            ns[BeaconFld.location.value],
                            ns[BeaconFld.freq.value],
                        )
                    )

            print("-" * 70)
            time.sleep(delay)
            tnow, delay = self.getdelay()
        self.logger.info("Loop run ended")

    def dump_band(self, band_id):
        self.logger.info(str.format("Dumping Band ID {}", band_id))
        for b in self.beacons:
            self.logger.info(str.format("Time offset {} ", b.band_time[band_id]))


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(" ")
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    dx = Beacons()
    dx.SetBand(int(sys.argv[3]))
    dx.beacon_start(timeout=5000)
    dx.dump_band(4)
