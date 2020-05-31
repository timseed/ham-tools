import logging

import serial

from .Io import Io


class P3(Io):
    """
    Commands with Internal functions removed

    = Product ID
    #AVG Averaging time
    #BCI Beacon interval
    #BCL Beacon location
    #BCN Beacon on/off
    #BMP Bitmap upload
    BR Baud rate set
    #BR Baud rate set
    #CAL Calibration signal on/off #CTF Center frequency #DSM Display mode
    #FNL Function key label
    Name Description
    #FNX Function key execute #FXA Fixed auto-adjust mode #FXT Fixed or Tracking select #KBMP Internal use only
    #LBL Labels on/off
    #LD Internal use only #MAA Marker A Adjust #MBA Marker B Adjust #MFA Marker A frequency #MFB Marker B frequency #MKA Marker A on/off #MKB Marker B on/off #MSS MSD Screen Shot #NB Noise blanker on/off #NBL Noise blanker Level #OSBA OSB Amplitude
    Name Description
    #OSBP OSB Phase
    #PKM Peak mode on/off
    #PS Power status/control #PT Pass-Through mode #QSY QSY to current marker #RCF Relative Center Freq. #REF Reference Level
    #RST Reset the PX3
    #RVM Main firmware revision #SCL Scale
    #SPN Span
    #TXH Text TX hang time #TXM Text TX Mode
    #USB USB connected?
    #VFB VFO B cursor on/off
    """

    def __init__(self, device="/dev/cu.usbserial-A7004VW8", baud_rate=38400, timeout=1):
        """
        Initialize the Radio. Supply the base parameters.
        After Flushing IO
        :param device:
        :param baud_rate:
        :param timeout:
        """
        self.logger = logging.getLogger(__name__)
        init = "PS"
        self.ser = self.open_serial(port=device, baud_rate=baud_rate, timeout=1)
        self.write(init)
        self.ser.flushInput()
        self.ser.flushOutput()

    def open_serial(
        self, port="/dev/cu.usbserial-A7004VW8", baud_rate=38400, timeout=1
    ):
        """
        Open the serial Device
        :param device:
        :param baud_rate:
        :param timeout:
        :return:
        """
        return serial.Serial(port=port, baudrate=baud_rate, timeout=1)

    def avg(self, time_in_secs: int) -> None:
        """
        Set the averaging time
        :param self:
        :param time_in_secs: average span in seconds
        :return: None
        """
        if 2 <= time_in_secs < 20:
            self.write("AVG{:02d};".format(time_in_secs))
        else:
            raise ValueError(f"Avg internal invalid {time_in_secs}")

    def avgq(self) -> str:
        """
        Get the time of the avg
        :return: str
        """
        self.write("#AVG;")
        result = self.read(7)
        if len(result) != 7:
            return "Unk"
        return result[4:-1]

    # todo this would be usedful
    def bmp(self):
        return None

    def baud_rate(self, speed: int) -> None:
        """
        Set the baud rate on the RS232 link

        :param speed: 0-4
        :return: None if success. Exception if incorrect.
        """
        if speed in [0, 1, 2, 3]:
            # format: BRn; or  # BRn; where n is 0 (4800 b), 1 (9600 b), 2 (19200 b), or 3 (38400 b). The PX3 Utility program automatically sets the PX3 to 38400 baud for downloads, then restores the baud rate to the user's selection (that was made using either this command or the PX3's RS232 menu entry). Note that the RS232 port that connects to the KX3 always runs at 38400 baud. Any BR command that is received from a host computer affects the baud rate of the PX3 (on the RS232 port that connects to the PC), not the KX3.
            return self.write("#BR{:1d};".format(speed))
        else:
            raise ValueError(f"Invalid Baud setting requested {speed}")

    # todo offsets not implemented yet
    def centre_freq(self, freq_in_hz: float) -> None:
        """
        Place the centre of the P3 at a known frequency.
        Note. Only valid Ham ranges are guaranteed.



        freq_in_hz means same freq as the VFO is currently on.
        :param freq_in_hz: 14060.123 or 0
        :return: None
        """
        # formatted string for 14060 would be
        # CTF+00014060000;
        if 0 <= freq_in_hz < 29000.0:
            f = int(freq_in_hz * 1000)
            self.write("#CTF+{:110d};".format(f))
        else:
            raise ValueError(f"Unknown frequency requested {freq_in_hz}")

    def centre_freqq(self) -> float:
        self.write("#CTF;")
        result = self.read(16)
        if len(result) != 16:
            return 0.0
        return float(result[4:-1]) / 1000.0

    def display_mode(self, mode: int) -> None:
        """
        0 (spectrum only) or 1 (spectrum + waterfall).
        :param mode:
        :return:
        """
        if mode in [0, 1]:
            return self.write("#DSM{:1d};".format(mode))
        else:
            raise ValueError(f"display_mode bad mode requested {mode}")

    def display_modeq(self) -> str:
        """
        Request what mode the display is currently in.
        :return: spectrum, spectrum/waterfall or Unk if error.
        """
        self.write("#DSM;")
        result = self.read(5)
        if len(result) != 5:
            return "Unk"
        return "spectrum" if result == "DSM0;" else "spectrum/waterfall"

    def nb(self, on_off: int):
        """
        Turn noise blanker on or off
        :param on_off: on = 1, off=0
        :return: None
        """
        if on_off in [0, 1]:
            # format: BRn; or  # BRn; where n is 0 (4800 b), 1 (9600 b), 2 (19200 b), or 3 (38400 b). The PX3 Utility program automatically sets the PX3 to 38400 baud for downloads, then restores the baud rate to the user's selection (that was made using either this command or the PX3's RS232 menu entry). Note that the RS232 port that connects to the KX3 always runs at 38400 baud. Any BR command that is received from a host computer affects the baud rate of the PX3 (on the RS232 port that connects to the PC), not the KX3.
            return self.write("#NB{:1d};".format(on_off))
        else:
            raise ValueError(f"Invalid Baud setting requested {on_off}")

    def nbq(self) -> str:
        """
        Return a string that indicates the Noise blanking setting.
        :return:  On, Off or Unk if something went wrong.
        """
        self.write("#NB;")
        result = self.read(4)
        if len(result) != 4:
            print(f"Err {result}")
            return "Unk"
        return "on" if result == "NM1;" else "off"

    def nbl(self, nb_level: int) -> None:
        """
        Set noise blanking level
        :param nb_level:
        :return:
        """
        if nb_level in range(1, 16):
            # format: BRn; or  # BRn; where n is 0 (4800 b), 1 (9600 b), 2 (19200 b), or 3 (38400 b). The PX3 Utility program automatically sets the PX3 to 38400 baud for downloads, then restores the baud rate to the user's selection (that was made using either this command or the PX3's RS232 menu entry). Note that the RS232 port that connects to the KX3 always runs at 38400 baud. Any BR command that is received from a host computer affects the baud rate of the PX3 (on the RS232 port that connects to the PC), not the KX3.
            return self.write("#NBL{:02d};".format(nb_level))
        else:
            raise ValueError(
                f"Invalid noise_blanking level setting requested {nb_level}"
            )

    def nblq(self) -> str:
        """
        Noice Blanker level
        :return:
        """
        self.write("#NBL;")
        result = self.read(9)
        if len(result) != 9:
            return "0"
        return result[4:-1]

    def fnl(self, key_id: int) -> str:
        """
        Get string setting for function key
        :param key_id: int 1-8
        :return: text of function key. Unk if error.
        """
        if key_id in range(1, 9):
            try:
                self.write("#FN{:1d};".format(key_id))
                result = self.read(14)
                if len(result) != 14:
                    return "Unk"
                else:
                    return result[4:-1]
            except Exception as err:
                return "Unk"

        else:
            raise ValueError(f"Function key invalid number {key_id}")
