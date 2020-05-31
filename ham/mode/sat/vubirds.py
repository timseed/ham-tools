"""
Small utility to Generate a CHIRP format CSV File.
"""

import logging
from dataclasses import dataclass


@dataclass
class SatFM:
    satname: str
    downlink_freq: float
    uplink_freq: float
    ctss_code: float
    activate_code: float


class VuBirds:
    """
    Very simple 2m/70cm Satellite configurator.
    """

    # This is the output file format
    # 6, Name, 145.800,-, 0.6,, 88.8, 88.5, 023, nm, FM, 5.00, S,, , , ,
    line = "{},{},{},off,5.000000,{},{},{},023,NN,FM,5.00,S,,,,,\n"

    def __init__(self, static_lines=None):
        """
        Setup the logger
        """
        self.logger = logging.getLogger()
        self.header = """Location,Name,Frequency,Duplex,Offset,Tone,rToneFreq,cToneFreq,DtcsCode,DtcsPolarity,Mode,TStep,Skip,Comment,URCALL,RPT1CALL,RPT2CALL,DVCODE
"""
        if static_lines:
            self.header += static_lines
        self.line_count = len(self.header.split("\n")) - 1

    def format_tone(self, tone: float) -> tuple:
        """
        The CSV Import in Chirp has a rather strange logic.
        You can not Specify None, and leave the Tone_Field Empty.
        You have to Specify a Tone (I picked 88.5), and just have the TONE_TYPE column set as Empty.

        :param tone: Float
        :return: Tuple('Tone_Type', TONE)
        """
        if tone > 0.0:
            return "Tone", tone
        else:
            return "", 88.5

    def process(
        self,
        sat_list=[
            SatFM(
                satname="AO51",
                downlink_freq=436.150,
                uplink_freq=144.200,
                ctss_code=0,
                activate_code=0,
            ),
            SatFM(
                satname="AO52",
                downlink_freq=437.150,
                uplink_freq=144.400,
                ctss_code=67,
                activate_code=97,
            ),
        ],
    ) -> str:
        """
        We need to generate data based in the sats list.
        This list is just a guess as to what you may need.

        :return: a CSV string that can be placed used in CHIRP.
        """
        self.logger.debug("Process called")

        output = self.header
        for s in sat_list:
            if s.activate_code > 0.0:
                # We need to "arm" the satellite
                # This means we transmit a special CTSS code to energize the satellite
                for channel in ["Arm"]:
                    dlf = VuBirds.simple_doppler(channel, s.downlink_freq)
                    tone, hz = self.format_tone(s.activate_code)
                    output += VuBirds.line.format(
                        self.line_count,
                        "{}-{}".format(s.satname, channel),  # Name
                        f"{dlf:9.6F}",  # Adjusted Freq
                        tone,
                        hz,
                        hz,
                    )
                    self.line_count += 1
            # We have 5 Channels  - AOS, Up, Top, Down, LOS
            for channel in ["A", "B", "C", "D", "E"]:
                dlf = VuBirds.simple_doppler(channel, s.downlink_freq)
                tone, hz = self.format_tone(s.ctss_code)
                output += VuBirds.line.format(
                    self.line_count,
                    "{}-{}".format(s.satname, channel),
                    f"{dlf:9.6F}",
                    tone,
                    hz,
                    hz,
                )
                self.line_count += 1
        return output

    @staticmethod
    def simple_doppler(chan: str, freq: float) -> float:
        """
        A very crude Doppler shift based on 5 points in the pass.

        :param chan: Str A....E (Including Arm)
        :param freq: In MHZ Downlink Freq in Mhz
        :return: Adjusted Frequency
        """

        if chan.startswith("A"):
            freq += 0.010
        elif chan.startswith("B"):
            freq += 0.005
        elif chan.startswith("D"):
            freq -= 0.005
        elif chan.startswith("E"):
            freq -= 0.01
        return freq
