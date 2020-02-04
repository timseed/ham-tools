import logging
import sys
from ham.beacon import Beacons

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)

    # add the handlers to the logger
    dx = Beacons(screenoutput=True)
    # dx.SetBand(int(sys.argv[1]))
    dx.beacon_start(timeout=5000)
    dx.dump_band(4)
    junk = 1
    junk = 1
