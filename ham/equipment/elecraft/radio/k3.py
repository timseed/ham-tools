#!/usr/bin/python
# Elecraft K2/K3 Rig Control Python Utilities
# Copyright (C) 2006-2011 Leigh L. Klotz, Jr <Leigh@WA5ZNU.org>
# Updated and modified by A45WG - a45wg@sy-edm.com
# Licensed under Academic Free License 3.0 (See LICENSE)


"""
Not all the functions in this modules have been tested - and not all appear to work as expected.

Further works remains here

"""

import logging

import serial
from .Io import Io


class K3(Io):
    def __init__(self, port="/dev/cu.usbserial-A7004VW8", baud_rate=38400, timeout=1):
        """
        Initialize the Radio. Supply the base parameters.
        After Flushing IO
        :param device:
        :param baud_rate:
        :param timeout:
        """
        self.logger = logging.getLogger(__name__)
        init = "PS"

        self.ser = self.open_serial(port=port, baud_rate=baud_rate, timeout=1)
        self.write(init)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.modeq()

    def open_serial(
        self, port="/dev/cu.usbserial-A7004VW8", baud_rate=38400, timeout=1
    ):
        """
        Open the serial Device
        :param port:
        :param baud_rate:
        :param timeout:
        :return:
        """
        return serial.Serial(port=port, baudrate=baud_rate, timeout=1)

    #
    # Set the VFO current frequency
    # FA00014060000
    # FA00007030000
    def qsy(self, freq: float) -> str:
        return self._qsy("a", freq)

    #
    # Set the 2ND RX VFO current frequency
    # FB00014060000
    # FB00007030000
    def qsy2(self, freq: float) -> str:
        return self._qsy("b", freq)

    def _qsy(self, band: str, freq: float) -> str:
        band = band.upper()
        if band not in ["A", "B"]:
            cmd = ""
            raise ValueError("Band code not a or b")
        else:
            if freq < 10e6:
                cmd = "F%s0000%d;" % (band,freq)  # in 7 digits
            elif freq > 10e6 and freq < 10e8:
                cmd = "F%s000%d;" % (band,freq)  # in 8 digits
            else:
                raise ValueError(f"Freq {freq} out of scope")
            self.write(cmd)
            return str(self.qsyq())

    def _qsyq(self, band: str) -> str:
        """

        :param band:
        :return:
        """
        band = band.upper()
        if band not in ["A", "B"]:
            raise ValueError("Band code not a or b")
        else:
            self.logger.debug(f"get VFO-{band}")
            self.write(f"F{band};")
            result = self.read(25)
            if len(result) >= 15:
                self.logger.debug("result is " + result)
                hz = result.split(";")[1].replace(f"F{band}", "")[0:8]
                # FA;FA00024893007;
                self.logger.debug(f"Hz read is <{hz}>")
                return hz
            else:
                return "0"

    #
    # Get the VFO current frequency
    # FA00014060000
    # FA00007030000
    def qsyq(self) -> str:
        return self._qsyq("A")

    def qsyq2(self) -> str:
        return self._qsyq("B")

    def fiq(self) -> str:
        """
        Get the First IF current frequency
        FI;
        FI6500;

        :return: string
        """
        self.write("FI;")
        result = self.read(7)
        if len(result) != 7:
            return "0"
        return "821" + result[2:3] + "." + result[3:6]

    # TODO: use SW22; to change thresh but we have to ready it first
    def nb(self, level, thresh) -> None:
        """
        Set the NB Threshold Level.
        :param level:
        :param thresh: 0-2. Off, 1, 2
        :return:
        """
        if 0 <= thresh <= 2:
            self.write("NB%s;" % level)
        else:
            raise ValueError(f"Invalid Threshold level {thresh}")

    def nbq(self) -> str:
        """

         Get the NB setting
         NB
         NB00; Off, hi thresh
         NB21; NB2, low thres
        :return:
        """
        self.write("NB;")
        result = self.read(5)
        if len(result) != 5:
            return "0"
        level = result[2]
        thresh = result[3]
        return "NB: %c %c" % (level, thresh)

    def mode(self, str_mode_setting: str) -> str:
        """
        Set the Mode.
        :param str_mode_setting: Input values are lsb usb cw cwr rtty
        :return: Output from method modeq
        """
        str_mode_setting = str_mode_setting.lower()
        mode_num: int = 0
        if str_mode_setting == "lsb" or str_mode_setting == "l":
            mode_num = 1
        elif str_mode_setting == "usb" or str_mode_setting == "u":
            mode_num = 2
        elif str_mode_setting == "cw" or str_mode_setting == "c":
            mode_num = 3
        elif str_mode_setting == "cwr":
            mode_num = 5
        elif str_mode_setting == "rtty" or str_mode_setting == "r":
            mode_num = 6
        elif str_mode_setting == "rttyr":
            mode_num = 9
        cmd = "MD%d" % mode_num
        self.write(cmd)
        return self.modeq()

    #
    # Get the mode
    def modeq(self) -> str:
        """
        Get the Mode that the radio is operating on
        :return: string to represent to mode. i.e. cw, ssb.
        """
        self.write("K22;MD")
        result = self.read(4)
        if len(result) != 4:
            return "???: " + result
        try:
            modenum = int(result[2])
        except ValueError:
            return "unk"
        if modenum == 1:
            return "lsb"
        elif modenum == 2:
            return "usb"
        elif modenum == 3:
            return "cw"
        elif modenum == 5:
            return "cwr"
        elif modenum == 6:
            return "rtty"
        elif modenum == 9:
            return "rttyr"
        else:
            return "???"

    def pa(self, pre_amp_setting: str = "on") -> str:
        """
            # Set the preamp
            # PA0; off
            # PA1; on

        :param pre_amp_setting:  on or off. Other values cause ValueError.
        :return: pre-amp-query -> Str
        """
        modenum = ""
        pre_amp_setting = pre_amp_setting.lower()
        if pre_amp_setting in ["on", "off"]:
            modenum = 1 if pre_amp_setting == "on" else 0
            cmd = "PA%d;" % modenum
            self.write(cmd)
            return self.paq()
        else:
            raise ValueError(f"Unknown pre-amp request {pre_amp_setting}")

    def paq(self) -> str:
        """
        Get the preamp
        :return: "0" Unknown, "on" or "off".
        """
        self.write("PA;")
        result = self.read(4)
        if len(result) != 4:
            return "0"
        if result == "PA1;":
            return "on"
        else:
            return "off"

    #
    # Set the power output
    # PC000; off
    # PC010; 10 watts
    def power(self, watts: int) -> str:
        cmd = "PC%03d;" % watts
        self.write(cmd)
        return self.powerq()

    #
    # Get the power output
    def powerq(self) -> str:
        self.write("PC;")
        result = self.read(6)
        if len(result) != 6:
            return "0"
        try:
            return str(int(result[1:4]) / 10)
        except ValueError:
            return "??"

    #
    # Set to VFO A for TX and RX
    def vfoa(self) -> str:
        self.write("FT0;FR0;")
        return self.vfoq()

    #
    # Get the B for TX and RX
    def vfob(self) -> str:
        self.write("FT1;FR1;")
        return self.vfoq()

    #
    # Get the VFO current frequency
    # FA00014060000
    # FA00007030000
    def vfoq(self) -> str:
        self.write("FT;FR;")
        result = self.read(8)
        if len(result) != 8:
            return "0"
        #    return "TX: %c; RX: %c" %(65+int(result[2]), 65+int(result[6]))
        return "Unk"

    #
    # Send CW
    # KY text;
    def sendcw_orig(self, cw_text: str) -> None:
        try:
            for a in cw_text.split(";"):
                cmd = a + ";"
                self.logger.debug("Sending " + cmd)
                self.write(cmd)
                self.logger.debug("CW Sent")
        except:
            logging.warning("sendcw issue")

    def sendcw(self, cw_text: str) -> None:
        try:
            self.logger.debug("Sending <" + cw_text + ">")
            self.write(cw_text)
            self.logger.debug("CW Sent")
        except:
            logging.warning("sendcw issue")

    def cwspeedq(self) -> int:
        """
        Get the CW Speed.

        K015; -> 15 wpm
        :return: string of wpm or 0
        """
        cmd = "KS;"
        self.write(cmd)
        result = self.read(5)
        if len(result) != 5:
            return 0
        try:
            return int(result[1:4])
        except ValueError:
            self.logger.error("Error converting cw speed")
            return 0

    def cwspeed(self, speed) -> int:
        """
        Set the CW Speed.

        :param speed:
        :return: Current CW speed as int
        """
        cmd = "K%3d;" % speed
        self.write(cmd)
        return self.cwspeedq()

    def ra(self, offon: int) -> str:
        """
        Set ATT to off=0|on=1
        :param offon:  int 0 off,1 on
        :return: str on, off or Unk
        """
        if 2 > offon >= 0:
            self.write("RA%:1d;".format(offon))
            return self.raq()
        else:
            raise ValueError(f"Invalid ra setting {offon}")

    def raq(self) -> str:
        """

        Get the ATT setting

        RA;
        RA00; off
        RA01; on
        :return: string on on, off or Unk
        """
        cmd = "RA;"
        self.write(cmd)
        result = self.read(5)
        if len(result) != 5:
            return "Unk"
        if result == "RA00;":
            return "off"
        elif result == "RA01;":
            return "on"
        else:
            return "Unk"

    #
    # Set the filter
    # 1, 2, 3, 4
    # FW00001;
    # 0 means "next"
    def filter(self, n) -> None:
        if n < 10:
            cmd = "FW0000%d;" % n
            self.write(cmd)
        else:
            raise ValueError(f"Filter number too large {n}")

    def filtern(self) -> str:
        """
        Get the filter number. If data invalid return "0"

        :return: str
        """
        self.write("FW;")
        result = self.read(9)
        if len(result) != 9:
            return str(0)
        return str(int(result[6]))

    #
    # Get the filter info
    def filterq(self) -> str:
        """
        Get the current Filter
        Returns a string in the format "nnnnHz n"

        :return: str
        """
        self.write("FW;")
        result = self.read(9)
        if len(result) != 9:
            return 0
        return result[2:6] + "Hz " + result[7]

    #
    # Get the display
    def displayq(self):
        return "Unused"

    #
    # Get the versions
    # RVM;
    # RVD;
    # RVA;
    # RVV;
    # RVF;
    # -> RV*nn.nn;
    def verq(self, x):
        self.write("RV%c;" % x)
        result = self.read(9)
        if len(result) != 9:
            return 0
        ver = result[3:8]
        if ver == "99.99":
            ver = None
        return ver

    def showtext(self, text: str) -> None:
        for letter in text:
            self.write("DB%s;" % letter)

    def k3lcdchar(self, c) -> str:
        if ord(c) > 127:
            return ":" + str(chr(ord(c) & 127))
        else:
            return str(c)

    def timeq(self) -> str:
        return "Unused"

    def fixtime(self) -> None:
        def k3LcdChar(c):
            return str(chr(ord(c) & 127))

    # TODO this does not work  - the documentation is incomplete. It has no effect and will return True.
    def set_channel(self, id: int, Name: str, Freq: float) -> bool:
        """
        MC (Memory Channel; GET/SET)
SET/RSP format: MCnnn; where nnn is the memory # (or channel). Regular memories are 000-099. Per-band
quickmemories: nnn=100+bandNum*4+Mn–1. ForbandNum,seeBN.Mnis1-4,i.e.         tap.
Notes: (1) A SET is ignored if the target memory is invalid. (2) K3 only: If CONFIG:MEM0-9 = BAND SEL, then memories 000-009 only (“Quick memories”) will recall the last-used VFO frequencies in the target band, not
fixed frequencies. (3) Switching to any regular memory (000-099) updates the K3’s default         memory
number; this is not the case when switching to Per-Band Quick memories (         ). (4) Switching to any memory
tagged with ‘*’ as the first character in its label enables channel-hop scanning (see K3/KX3/KX2 Owner’s manual).
        :param id:
        :param Name:
        :param Freq:
        :return:
        """
        # self.qsy(Freq)
        # self.write("MC{:03d};".format(id))
        # result = self.read(3)
        # if len(result) != 3:
        #     return False
        return True

    def use_channel(self, id: int) -> int:
        self.write("MC{:03d};".format(id))
        return True

    def read_data(self,no_of_chars=20):
        return self.read(no_of_chars)


    def set_band(self, band_number:int) -> str:
        self.write("BN{:02d};".format(band_number))
        return self.get_band()

    def get_band(self) ->str:
        self.write("BN;")
        result = self.read(4)
        if len(result) != 4:
            return "Unk"
        return result[2:]
