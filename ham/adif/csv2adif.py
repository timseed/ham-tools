"""
Convert Csv to Adif
"""

import csv


class Csv2Adif(object):
    def __init__(self):
        self.filename = None

    def process(self, filename: str):
        self.filename = filename
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                line = ""
                for fld in reader.fieldnames:
                    if len(row[fld].strip()) > 0:
                        line = line + str.format(
                            "<{}:{}>{} ", fld, len(row[fld].strip()), row[fld].strip()
                        )

                yield line + " <eor>"
        csvfile.close()
