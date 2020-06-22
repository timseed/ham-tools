import logging
import sys
import daiquiri


def set_logging(levelwanted=logging.INFO):
        format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        formatter1 = logging.Formatter(format_str, date_format)
        daiquiri.setup(
            level=levelwanted,
            outputs=(
                daiquiri.output.Stream(sys.stdout, formatter=formatter1),
                daiquiri.output.File(
                    f"{__name__}.log", formatter=formatter1
                ),
            ),
        )
        my_logger = daiquiri.getLogger()
        return my_logger
