# from ham.adif.adif2csv import adif2csv
from ham.adif.csv2adif import Csv2Adif
from ham.beacon import *
from ham.qsosvr.dxspider import dxspider
from ham.rbn.rbn import Rbn
from ham.dxcc import dxcc_country
from ham.dxcc.dxcc_country import DxCc


def dxcc_tests():
    d = dxcc_country()
    d.read()
    d.showall()
    # d.show('G')
    # d.show('F')
    d.show("M0FGC")


def adif_tests():
    """
    csv and adif testing
    """
    cvt = adif2csv(all_lines_same=False)
    cvt.process("asian2006.adif")
    for a in cvt.dump():
        print("" + a)

    cvt2 = Csv2Adif("asian2006.csv")
    for a in cvt2.process():
        print("" + a)


def beacon_tests():
    """
    Beacons testing
    """

    dx = beacons(ScreenOutput=True)
    dx.SetBand(14)
    dx.beacon_start(timeout=50)
    dx.dump_band(4)
    junk = 1


def dxspider_tests():
    host = "gb7mbc.spoo.org"
    port = 8000
    call = "a45wg"
    dxs = dxspider(host, port, call)
    if dxs.do_connect():
        for i in range(2000):
            dxs.get_dx()


def rbn_tests():
    r = Rbn()
    r.loop()


# dxcc_tests()
# adif_tests()
# beacon_tests()
# dxspider_tests()
rbn_tests()

print("Finished Tests")
