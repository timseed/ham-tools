import yaml
import logging
import serial
from time import sleep
import collections
from typing import Optional


class Kpa500(object):
    def __init__(self, config_file: str) -> None:

        b = [160, 80, 60, 40, 30, 20, 17, 15, 12, 10, 6]
        self.Bands = {}
        self.logger = logging.getLogger(__name__)
        tmp = 0
        for bb in b:
            self.Bands[bb] = "{:02d}".format(tmp)
            tmp = tmp + 1

        # Commands, their English Meaning, a Place to store their value, and what datatype they should be, Plus ReadWrite Allowed
        ucmd = {
            "^AL": {
                "Msg": "Alc Value",
                "Value": "",
                "Type": int,
                "RW": True,
                "Fmt": '"ALC {:03d}',
            },
            "^AR": {
                "Msg": "Attenuator Fault Release Time",
                "Value": "",
                "Type": int,
                "RW": True,
                "Fmt": '"ALC {:03d}',
            },
            "^BC": {
                "Msg": "StandBy on Band Change",
                "Value": "",
                "Type": int,
                "RW": True,
                "Fmt": '"ALC {:03d}',
            },
            "^BN": {
                "Msg": "Band Selection",
                "Value": "",
                "Type": int,
                "RW": True,
                "Fmt": '"ALC {:03d}',
            },
            "^BRP": {
                "Msg": "RS232 PC port data rate",
                "Value": "",
                "Type": int,
                "RW": True,
            },
            "^BRX": {
                "Msg": "RS232 XCVR port data rate",
                "Value": "",
                "Type": int,
                "RW": True,
            },
            "^DMO": {"Msg": "DEMO mode", "Value": "", "Type": int, "RW": True},
            "^FC": {"Msg": "Fan Minimum Control", "Value": "", "Type": int, "RW": True},
            "^FL": {"Msg": "Current Fault", "Value": "", "Type": int, "RW": True},
            "^NL": {
                "Msg": "Enable Inhibit Input",
                "Value": "",
                "Type": int,
                "RW": True,
            },
            "^ON": {"Msg": "Power Status & Off", "Value": "", "Type": int, "RW": True},
            "^OS": {"Msg": "OP/STBY", "Value": "", "Type": int, "RW": True},
            "^PJ": {"Msg": "Power Adjustment", "Value": "", "Type": int, "RW": True},
            "^RVM": {
                "Msg": "Firmware Release identifier",
                "Value": "",
                "Type": int,
                "RW": False,
            },
            "^SN": {"Msg": "Serial Number", "Value": "", "Type": int, "RW": False},
            "^SP": {
                "Msg": "Fault Speaker On/Off",
                "Value": "",
                "Type": int,
                "RW": True,
            },
            "^TM": {"Msg": "PA Temperature", "Value": "", "Type": int, "RW": False},
            "^TR": {"Msg": "T/R Delay Time", "Value": "", "Type": int, "RW": True},
            "^VI": {"Msg": "PA Volts/Current", "Value": "", "Type": int, "RW": False},
            "^WS": {"Msg": "Power/SWR", "Value": "", "Type": int, "RW": False},
            "^XI": {"Msg": "Radio Interface", "Value": "", "Type": int, "RW": True},
        }
        self.cmd = collections.OrderedDict(sorted(ucmd.items()))

        self.l = logging.getLogger(__name__)
        with open(config_file, "r") as ymlfile:
            self.logger.debug("Opened file " + config_file)
            cfg = yaml.load(ymlfile)
            try:
                self.device = cfg["Kpa500"]["device"]
                self.logger.debug("Read Yaml device set to {}".format(self.device))
            except Exception as e:
                self.logger.error(
                    "Could not get value for Kpa500:device from config file" + str(e)
                )
            try:
                self.speed = cfg["Kpa500"]["speed"]
                self.logger.debug("Read Yaml speed set to {}".format(self.speed))
            except Exception as e:
                self.logger.error(
                    "Could not get value for Kpa500:speed from config file" + str(e)
                )

        try:
            self.logger.debug(
                "Trying to connect to the Serial device {}".format(self.device)
            )
            self.serial_port = serial.Serial(port=self.device, baudrate=self.speed)
            if self.serial_port.is_open:
                self.logger.info("Connected to {} OK".format(self.serial_port))

        except Exception as e:
            self.logger.error(
                "Error connecting to {}: Error is {}".format(self.device, str(e))
            )

    @property
    def read_kpa(self):
        self.logger.debug("read_kpa being called")

    @property
    def get_alc(self):
        try:
            self.logger.debug("Trying to get the ALC Value")
            self.serial_port.write("^ALC".encode())
            self.logger.debug("Now Read the ALC Value")
            val = self.serial_port.read_all()
            self.logger.debug("ALC Got {}".format(val))
        except Exception as e:
            self.logger.error("Error in ALC Function Error is {}".format(str(e)))

    @property
    def get(self, command, english_command):
        try:
            self.logger.debug(
                "Trying to get the {} using Code {}".format(english_command, command)
            )
            written = self.serial_port.write(command.encode())
            self.logger.debug("Now Read the {} Value".format(english_command))
            sleep(0.3)
            val = self.serial_port.read_all()
            val = val.decode()
            self.logger.debug("{} Got {}".format(command, val))
            return val
        except Exception as e:
            self.logger.error(
                "Error in {} Function Error is {}".format(command, str(e))
            )

    # @property
    # def get_all(self):
    #     self.logger.debug("In get_All")
    #     for ky in self.cmd.keys():
    #         self.get(ky + ";", self.cmd[ky]["Msg"])

    @property
    def write(self, cmd):
        """ The user should have seen this on screen already """
        return self.serial_port.write(cmd.encode())

    @property
    def get_band(self) -> Optional[str]:
        try:
            self.logger.debug("Trying to set the Band Value")
            self.serial_port.write("^BN06;".encode())
            self.logger.debug("Now Read the BN Value")
            val = self.serial_port.read_all()
            self.logger.debug("BN Got {}".format(val))
            return val
        except Exception as e:
            self.logger.error("Error in BN Function Error is {}".format(str(e)))
