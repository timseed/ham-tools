import daiquiri
import re


class Csv2Cab:

    def __init__(self):
        self.logger = daiquiri.getLogger(__name__)
        self.logger.debug("init Csv2Cab")
