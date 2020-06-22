from ham.cabrillo.cab2csv import Cab2Csv
from ham.log import set_logging
import argparse
import os
import logging
import daiquiri


def file_exists(x):
    """
    'Type' for argparse - checks that file exists but does not open.
    """
    if not os.path.exists(x):
        # Argparse uses the ArgumentTypeError to give a rejection message like:
        # error: argument input: x does not exist
        raise argparse.ArgumentTypeError("{0} does not exist".format(x))
    return x


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Cab to ADIF")
    parser.add_argument(
        "-i",
        "--input",
        dest="file",
        required=True,
        metavar="FILE",
        type=file_exists,
        help="Cab file to read",
    )

    parser.add_argument(
        "-o",
        "--output",
        dest="outfile",
        required=True,
        metavar="FILE",
        help="Cab file to write to",
    )

    parser_group = parser.add_mutually_exclusive_group(required=False)
    parser_group.add_argument(
        "-v",
        "--WAR",
        dest="logging_level",
        default=logging.WARNING,
        action="store_const",
        const=logging.WARNING,
    )
    parser_group.add_argument(
        "-vv", "--INF", dest="logging_level", action="store_const", const=logging.INFO
    )
    parser_group.add_argument(
        "-vvv", "--DEB", dest="logging_level", action="store_const", const=logging.DEBUG
    )
    args = parser.parse_args()
    LOGGER  = set_logging(logging.INFO)
    cab = Cab2Csv()
    lines = cab.read_cab(args.file)
    qsos = cab.produce_qso(lines)
    with open(args.outfile, "at") as ofp:
        ofp.write(cab.to_adif(qsos))
    LOGGER.debug(f"Adif {args.outfile} created ")
