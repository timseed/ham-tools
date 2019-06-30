import yaml
import logging
import serial
from collections import namedtuple
from time import sleep
import collections


class kpa500cls(object):
    def __init__(self, config_file):

        b = [160, 80, 60, 40, 30, 20, 17, 15, 12, 10, 6]
        self.Bands = {}

        tmp = 0
        for bb in b:
            self.Bands[bb] = "{:02d}".format(tmp)
            tmp = tmp + 1

        # Commands, their English Meaning, a Place to store their value, and what datatype they should be, Plus ReadWrite Allowed
        ucmd = {'^AL': {'Msg': 'Alc Value', 'Value': '', 'Type': int, 'RW': True, 'Fmt': '"ALC {:03d}'},
                '^AR': {'Msg': 'Attenuator Fault Release Time', 'Value': '', 'Type': int, 'RW': True,
                        'Fmt': '"ALC {:03d}'},
                '^BC': {'Msg': 'StandBy on Band Change', 'Value': '', 'Type': int, 'RW': True, 'Fmt': '"ALC {:03d}'},
                '^BN': {'Msg': 'Band Selection', 'Value': '', 'Type': int, 'RW': True, 'Fmt': '"ALC {:03d}'},
                '^BRP': {'Msg': 'RS232 PC port data rate', 'Value': '', 'Type': int, 'RW': True},
                '^BRX': {'Msg': 'RS232 XCVR port data rate', 'Value': '', 'Type': int, 'RW': True},
                '^DMO': {'Msg': 'DEMO mode', 'Value': '', 'Type': int, 'RW': True},
                '^FC': {'Msg': 'Fan Minimum Control', 'Value': '', 'Type': int, 'RW': True},
                '^FL': {'Msg': 'Current Fault', 'Value': '', 'Type': int, 'RW': True},
                '^NL': {'Msg': 'Enable Inhibit Input', 'Value': '', 'Type': int, 'RW': True},
                '^ON': {'Msg': 'Power Status & Off', 'Value': '', 'Type': int, 'RW': True},
                '^OS': {'Msg': 'OP/STBY', 'Value': '', 'Type': int, 'RW': True},
                '^PJ': {'Msg': 'Power Adjustment', 'Value': '', 'Type': int, 'RW': True},
                '^RVM': {'Msg': 'Firmware Release identifier', 'Value': '', 'Type': int, 'RW': False},
                '^SN': {'Msg': 'Serial Number', 'Value': '', 'Type': int, 'RW': False},
                '^SP': {'Msg': 'Fault Speaker On/Off', 'Value': '', 'Type': int, 'RW': True},
                '^TM': {'Msg': 'PA Temperature', 'Value': '', 'Type': int, 'RW': False},
                '^TR': {'Msg': 'T/R Delay Time', 'Value': '', 'Type': int, 'RW': True},
                '^VI': {'Msg': 'PA Volts/Current', 'Value': '', 'Type': int, 'RW': False},
                '^WS': {'Msg': 'Power/SWR', 'Value': '', 'Type': int, 'RW': False},
                '^XI': {'Msg': 'Radio Interface', 'Value': '', 'Type': int, 'RW': True}
                }
        self.cmd = collections.OrderedDict(sorted(ucmd.items()))

        self.l = logging.getLogger(__name__)
        with open(config_file, 'r') as ymlfile:
            self.dbg("Opened file " + config_file)
            cfg = yaml.load(ymlfile)
            try:
                self.device = cfg['kpa500cls']['device']
                self.dbg('Read Yaml device set to {}'.format(self.device))
            except Exception as e:
                self.err('Could not get value for kpa500cls:device from config file' + str(e))
            try:
                self.speed = cfg['kpa500cls']['speed']
                self.dbg('Read Yaml speed set to {}'.format(self.speed))
            except Exception as e:
                self.err('Could not get value for kpa500cls:speed from config file' + str(e))

        try:
            self.dbg("Trying to connect to the Serial device {}".format(self.device))
            self.serial_port = serial.Serial(port=self.device, baudrate=self.speed)
            if self.serial_port.is_open:
                self.info('Connected to {} OK'.format(self.serial_port))

        except Exception as e:
            self.err('Error connecting to {}: Error is {}'.format(self.device, str(e)))

    def info(self, msg):
        self.l.info(msg)

    def dbg(self, msg):
        self.l.debug(msg)

    def err(self, msg):
        self.l.error(msg)

    def read_kpa(self):
        self.dbg('read_kpa being called')

    def getALC(self):
        try:
            self.dbg('Trying to get the ALC Value')
            self.serial_port.write('^ALC'.encode())
            self.dbg('Now Read the ALC Value')
            val = self.serial_port.read_all()
            self.dbg('ALC Got {}'.format(val))
        except Exception as e:
            self.err('Error in ALC Function Error is {}'.format(str(e)))

    def get(self, Command, EnglishCommand):
        try:
            self.dbg('Trying to get the {} using Code {}'.format(EnglishCommand, Command))
            written = self.serial_port.write(Command.encode())
            self.dbg('Now Read the {} Value'.format(EnglishCommand))
            sleep(0.3)
            val = self.serial_port.read_all()
            val = val.decode()
            self.dbg('{} Got {}'.format(Command, val))
            return val
        except Exception as e:
            self.err('Error in {} Function Error is {}'.format(Command, str(e)))

    def get_All(self):
        self.dbg("In get_All")
        for ky in self.cmd.keys():
            self.get(ky + ';', self.cmd[ky]['Msg'])

    def write(self,cmd):
       ''' The user should have seen this on screen already '''
       self.serial_port.write(cmd.encode())


    def setBand(self):
        try:
            self.dbg('Trying to set the Band Value')
            self.serial_port.write('^BN06;'.encode())
            self.dbg('Now Read the BN Value')
            val = self.serial_port.read_all()
            self.dbg('BN Got {}'.format(val))
        except Exception as e:
            self.err('Error in BN Function Error is {}'.format(str(e)))


if __name__ == "__main__":

    import yaml
    import logging
    import logging.config
    from time import sleep
    import pprint

    with open('logging.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
        log = logging.getLogger(__name__)
        linear = kpa500cls('config.yaml')
        # linear.setBand()
        # sleep(1)
        # linear.get('^BN;','Band Mode')
        #linear.get_All()
        pprint.pprint(linear.cmd)
        for k in linear.cmd.keys():
            print("k: {}".format(k))
        print("Number of keys is {}".format(len(linear.cmd.keys())))
        print("======RW=====")
        t=[]
        for k in linear.cmd.keys():
            if linear.cmd[k]['RW']==True:
                t.append(k)
        pprint.pprint(t)
        print("Keys with True are {}".format(len(t)))

