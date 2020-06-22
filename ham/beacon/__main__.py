import logging
import sys
import daiquiri
from ham.beacon import Beacons, SetK3Freq
from ham.log import set_logging

if __name__ == "__main__":
    import argparse


    # Try and set the K3 for the Bands
    parser = argparse.ArgumentParser(description='K3 Set to Beacon or CW Freq.')
    parser.add_argument("-m",
                        "--mode",
                        help="What mode ? Cw or Beacon",
                        required=False,
                        dest='beacon',
                        default="beacon",
                        type=str)

    parser_group = parser.add_mutually_exclusive_group(required=False)
    parser_group.add_argument("-v",
                              "--WAR",
                              dest='logging_level',
                              default=logging.WARNING,
                              action='store_const',
                              const=logging.WARNING
                              )
    parser_group.add_argument("-vv",
                              "--INF",
                              dest='logging_level',
                              action='store_const',
                              const=logging.INFO
                              )
    parser_group.add_argument("-vvv",
                              "--DEB",
                              dest='logging_level',
                              action='store_const',
                              const=logging.DEBUG
                              )
    args = parser.parse_args()
    logger = set_logging(args.logging_level)
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
