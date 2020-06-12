import logging
import sys
import daiquiri
from ham.beacon import Beacons, SetK3Freq

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    # Try and set the K3 for the Bands
    try:
        sk3 = SetK3Freq(mode='beacon')
        logger.info("K3 Setup")
    except Exception as err:
        logger.error(f"Problem {err} setting K3 Beacon frequencies")
        pass
    # add the handlers to the logger
    dx = Beacons(screenoutput=True)
    # dx.SetBand(int(sys.argv[1]))
    dx.beacon_start(timeout=5000)
    dx.dump_band(4)
