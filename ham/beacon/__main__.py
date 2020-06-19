import logging
import sys
import daiquiri
from ham.beacon import Beacons, SetK3Freq

if __name__ == "__main__":
    import argparse
    logger = logging.getLogger(__name__)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    # Try and set the K3 for the Bands
    parser = argparse.ArgumentParser(description='Beacons')
    # parser.add_argument('-b',
    #                     '--band', dest='band',
    #                     required=False,
    #                     default=14,
    #                     help='Band i.e. 14 21 28 ')

    parser.add_argument("-m",
                        "--mode",
                        help="What mode ? Cw or Beacon",
                        required=False,
                        dest='beacon',
                        default="beacon",
                        type=str)
    args = parser.parse_args()
    logger.info(f"Setting mode to {args.beacon}")
    try:
        sk3 = SetK3Freq(mode=args.beacon)
        logger.info("K3 Setup")
    except Exception as err:
        logger.error(f"Problem {err} setting K3 Beacon frequencies")
        pass
    # add the handlers to the logger
    dx = Beacons(screenoutput=True)
    # dx.SetBand(int(sys.argv[1]))
    dx.beacon_start(timeout=5000)
    dx.dump_band(4)
