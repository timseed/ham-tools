import socket, select, sys
import logging
from datetime import datetime
from ham.qsosvr import dxspider
from ham.log import set_logging
# todo needs argparse

logger  = set_logging()
if len(sys.argv) < 3:
    print("Usage : python telnet.py hostname port callsign")
    print("Defaulting to gb7mbc.spoo.org 8000 a45wg")
    print("got {} args".format(len(sys.argv)))
    host = "gb7mbc.spoo.org"
    port = 8000
    call = "a45wg"

    # dxc.nc7j.com 7300
    # olson.net.nz 9000 - was not working
    # zl2arn.dyndns.org:7300
else:
    host = sys.argv[1]
    port = int(sys.argv[2])
    call = sys.argv[3]

dxs = dxspider(host, port, call)
if dxs.do_connect():
    for i in range(2000):
        dxs.get_dx()
