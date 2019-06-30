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


class K3:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        device = "/dev/cu.usbserial-A7004VW8"
        baudrate = 38400
        init = "PS"
        self.ser = serial.Serial(device, baudrate=baudrate, timeout=1)
        self.write(init)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.modeq()

    def close(self):
        self.ser.flushInput()  # until the "quit" comes along.
        self.ser.close()

    def write(self, str_command: str) -> None:
        for a in str_command.split(';'):
            self.logger.debug("Sending Data to Serial Port")
            self.ser.write((a + ';').encode('utf-8'))
            # self.ser.flushInput()

    def read(self, bytes_to_read: int) -> str:
        try:
            return self.ser.read(bytes_to_read).decode('utf-8')
        except:
            self.logger.error("Error Reading data")
            return ''

    #
    # Set the VFO current frequency
    # FA00014060000
    # FA00007030000
    def qsy(self, freq: float) -> str:
        if freq < 10e6:
            cmd = "FA0000%d;" % freq  # in 7 digits
        else:
            cmd = "FA000%d;" % freq  # in 8 digits
        self.write(cmd)
        return self.qsyq()

    #
    # Set the 2ND RX VFO current frequency
    # FB00014060000
    # FB00007030000
    def qsy2(self, freq: float) -> str:
        if freq < 10e6:
            cmd = "FB0000%d;" % freq  # in 7 digits
        else:
            cmd = "FB000%d;" % freq  # in 8 digits
        self.write(cmd)
        return str(self.qsyq())

    #
    # Get the VFO current frequency
    # FA00014060000
    # FA00007030000
    def qsyq(self) -> str:
        # self.ser.flushOutput()
        # self.ser.flushInput()
        self.logger.debug("get VFO-A")
        self.write("FA;")
        result = self.read(20)
        if len(result) > 15:
            self.logger.debug("result is " + result)
            hz = result.split(';')[2].replace('FA', '')[0:8]
            # FA;FA00024893007;
            return hz
        else:
            return "0"

    #
    # Get the 2ND RX VFO current frequency
    # FA00014060000
    # FA00007030000
    def qsyq2(self) -> str:
        self.logger.debug("Get VFO-B")
        self.write("FB;")
        result = self.read(20)
        if len(result) > 15:
            self.logger.debug("result is " + result)
            hz = result.split(';')[2].replace('FB', '')[0:8]
            # FA;FA00024893007;
            return hz
        else:
            return "0"

    #
    # Get the First IF current frequency
    # FI;
    # FI6500;
    def fiq(self) -> str:
        self.write("FI;")
        result = self.read(7)
        if len(result) != 7:
            return "0"
        return "821" + result[2:3] + "." + result[3:6]

    #
    # Set NB to level (off=0, 1, 2)
    # TODO: use SW22; to change thresh but we have to ready it first
    def nb(self, level, thresh):
        self.write("NB%s;" % level)

    #
    # Get the NB setting
    # NB
    # NB00; Off, hi thresh
    # NB21; NB2, low thres
    def nbq(self) -> str:
        self.write("NB;")
        result = self.read(5)
        if len(result) != 5:
            return "0"
        level = result[2]
        thresh = result[3]
        return "NB: %c %c" % (level, thresh)

    #
    # Set the Mode
    # MD1; LSB
    # FA00007030000
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
        cmd = "MD%d;" % mode_num
        self.write(cmd)
        return self.modeq()

    #
    # Get the mode
    def modeq(self) -> str:
        self.write("K22;MD;")
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

    #
    # Set the preamp
    # PA0; off
    # PA1; on
    def pa(self, pre_amp_setting='on') -> str:
        modenum = ""
        if pre_amp_setting.lower() == "off":
            modenum = 0
        if pre_amp_setting.lower() == "on":
            modenum = 1
        cmd = "PA%d;" % modenum
        self.write(cmd)
        return self.paq()

    #
    # Get the preamp
    def paq(self) -> str:
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
            for a in cw_text.split(';'):
                cmd = a + ';'
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

    # TODO
    # Set speed 15=K015;
    def cwspeedq(self) -> str:
        cmd = "KS;"
        self.write(cmd)
        result = self.read(5)
        if len(result) != 5:
            return "0"
        return result[1:3]

    # TODO
    def cwspeed(self, speed) -> str:
        cmd = "K%3d;"
        self.write(cmd)
        return self.cwspeedq()

    #
    # Set ATT to off=0|on=1
    def ra(self, offon) -> str:
        return "Unused"

    #
    # Get the ATT setting
    # RA;
    # RA00; off
    # RA01; on
    def raq(self):
        return "Unused"

    #
    # Set the filter
    # 1, 2, 3, 4
    # FW00001;
    # 0 means "next"
    def filter(self, n):
        cmd = "FW0000%d;" % n
        self.write(cmd)

    #
    # Get the filter number
    def filtern(self):
        self.write("FW;")
        result = self.read(9)
        if len(result) != 9:
            return str(0)
        return str(int(result[6]))

    #
    # Get the filter info
    def filterq(self):
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
        if ver == '99.99':
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


if __name__ == "__main__":
    import sys

    testmode = int(sys.argv[1])
    rig = K3()
    if testmode == 1:
        print("testing K3")
        print("What Mode")
        print('' + rig.modeq())
        print("Check PreAmp")
        print('' + rig.paq())
        print("PreAmp on")
        print('' + rig.pa("on"))
        print("VFO-A")
        print('' + rig.qsyq())
        print("VFO-B")
        print('' + rig.qsyq2())
        print("FIQ")
        print('' + rig.fiq())
        print("Noise Blocker-A")
        print('' + rig.nbq())
        print("Mode")
        print('' + rig.modeq())
        print("Pre Amp")
        print('' + rig.paq())
        print("Power Settings")
        print('' + rig.powerq())
        print("VFO")
        print('' + rig.vfoq())
        print("CW Speed")
        print('' + rig.cwspeedq())
        print("RA ")
        print('' + rig.raq())
        print("Filter")
        print('' + rig.filterq())
        print("Display")
        print('' + rig.displayq())
        # print("Ver")
        # print('' + rig.verq(, x))
        print("Time")
        print('' + rig.timeq())
        print("Tests Finished")
    elif testmode == 0:
        rig.modeq()
        print("About to send")
        from time import sleep

        rig.sendcw("KYW hi there;")
        sleep(3)
        print("Done")
    elif testmode == 3:
        #        print(''+rig.modeq(),end='\n')
        print('' + rig.qsyq(), end='\n')
        print("Done")
