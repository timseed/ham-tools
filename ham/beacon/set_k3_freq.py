"""
I would like to set the correct frequencies into each of the 5 bands
on the K3, so I can auto switch band, to check if the station is still available.

As the Station first appears on 20m, and then 17 and then 15. It should be
pre-programmed.

"""
import logging
import sys
import daiquiri

from time import sleep

from ham.equipment.elecraft.radio import k3


class SetK3Freq:

    def __init__(self, mode='beacon'):
        self.logger = daiquiri.getLogger(__name__)
        self.logger.debug("SetK3Freq initialized")
        self.cw_freq = [14025000,
                        18072000,
                        21020000,
                        24915000,
                        28025000]
        self.beacon_freq = [
            14100000,
            18110000,
            21150000,
            24930000,
            28200000]
        self.band = [5, 6, 7, 8, 9]
        if mode == 'beacon':
            self.logger.info("Setting up Beacon frequencies")
            self.set_freq(self.beacon_freq)
        else:
            self.logger.info("Setting up Cw frequencies")
            self.set_freq(self.cw_freq)

    def set_freq(self, list_of_freq):
        self.logger.debug("Initialize the K3")
        my_radio = k3.K3()

        for i in range(0, len(list_of_freq)):
            junk = my_radio.read_data()

            band_now = my_radio.set_band(self.band[i])
            self.logger.debug(f"Band now {band_now}")
            f = list_of_freq[i]
            mode_is = my_radio.mode(str_mode_setting='cw')
            self.logger.debug(f"Mode set to  {mode_is}")

            self.logger.debug(f"Try to QSY to {f / 1000000} Mhz")
            freq_tuned_too = my_radio.qsy(freq=f)
            sleep(0.1)

            self.logger.info(f"Tuned to  {freq_tuned_too} Khz")


if __name__ == "__main__":

    format_str = '%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s'
    date_format = "%Y-%m-%d %H:%M:%S"
    formatter1 = logging.Formatter(format_str, date_format)

    daiquiri.setup(outputs=(
        daiquiri.output.Stream(sys.stdout, formatter=formatter1),
    ),
        level=logging.INFO,
    )
    logger = daiquiri.getLogger()
    logger.debug("All set")
    sk3 = SetK3Freq()
    logger.info("All Done")
