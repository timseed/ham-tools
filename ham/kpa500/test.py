from kpa0500 import kpa500
import yaml
import logging
import logging.config
from time import sleep

with open('logging.yaml', 'rt') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    log = logging.getLogger(__name__)
    linear = kpa500cls('config.yaml')
    # linear.setBand()
    # sleep(1)
    # linear.get('^BN;','Band Mode')
    linear.get_All()