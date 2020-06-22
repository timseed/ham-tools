import yaml
import logging
import pprint
from ham.equipment.elecraft.kpa500 import Kpa500
from ham.log import set_logging

log = set_logging(logging.INFO)
linear = Kpa500("config.yaml")
# linear.setBand()
# sleep(1)
# linear.get('^BN;','Band Mode')
# linear.get_All()
pprint.pprint(linear.cmd)
for k in linear.cmd.keys():
    print("k: {}".format(k))
print("Number of keys is {}".format(len(linear.cmd.keys())))
print("======RW=====")
t = []
for k in linear.cmd.keys():
    if linear.cmd[k]["RW"] == True:
        t.append(k)
pprint.pprint(t)
print("Keys with True are {}".format(len(t)))
