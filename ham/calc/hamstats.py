import logging
from ham.band import HamBand
from ham.dxcc import DxccAll
from datetime import datetime


class WorkedCountries(object):
    """
    Wrapper Class to produce a list of Countries for ALL HF Bands that you may want to Work
    This is not: MODE specific
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        hb = HamBand()
        d = DxccAll()
        status = [False]

        status = [False]
        self.Countries_Band_To_Work = {}

        for c in d.countrylist:
            self.Countries_Band_To_Work[c] = {}
            for b in hb.Band:
                for s in status:
                    self.Countries_Band_To_Work[c][b] = {}
                    self.Countries_Band_To_Work[c][b] = {"status": s}


class ContestCountries(WorkedCountries):
    """
    Wrapper class for Contest Work
    Assumes you are only trying to work the Contest Bands per Countries
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.hb = HamBand()
        d = DxccAll()
        d.read()
        Status = [0]

        self.Countries_Band_To_Work = {}
        for c in d.countrylist:
            self.Countries_Band_To_Work[c] = {}
            for b in self.hb.Band:
                for s in Status:
                    self.Countries_Band_To_Work[c][b] = {}
                    self.Countries_Band_To_Work[c][b] = {"status": s}

    def process(self, filename):
        """
        Process expects a filename - in this file there should be the following fields.
                                        datetime.now().isoformat(),
                                        BAND
                                        MODE
                                        CALL
                                        RST
                                        SENT
                                        RECEIVE
                                        COUNTRY_NAME
        """

        now = datetime.now()
        last_1_hour = 0
        last_2_hour = 0
        last_4_hour = 0

        with open(filename, "rt") as f:
            for line in f:
                (
                    qsodate,
                    band,
                    mode,
                    call,
                    rst,
                    sent,
                    receive,
                    country_name,
                ) = line.split(",")
                country_name = country_name.lstrip().rstrip()
                try:
                    self.Countries_Band_To_Work[country_name][int(band)]["status"] = (
                        self.Countries_Band_To_Work[country_name][int(band)]["status"]
                        + 1
                    )
                    qso_datetime = datetime.strptime(qsodate, "%Y-%m-%dT%H:%M:%S.%f")
                    hourssince = int((now - qso_datetime).seconds / 3600)
                    if hourssince <= 4:
                        last_4_hour = last_4_hour + 1
                        if hourssince <= 2:
                            last_2_hour = last_2_hour + 1
                            if hourssince <= 1:
                                last_1_hour = last_1_hour + 1
                except Exception as e:
                    self.logger.error(
                        "Problem with stats for a record {} {}".format(line, str(e))
                    )
            f.close()

        # Now Per band country the unique countries
        band_items = len(self.hb.Band)
        band_ctry_qso_totals = [0 for a in range(band_items)]
        band_qso_totals = [0 for a in range(band_items)]

        bpos = 0
        for b in self.hb.Band:
            for c in self.Countries_Band_To_Work:
                if self.Countries_Band_To_Work[c][b]["status"] > 0:
                    band_ctry_qso_totals[bpos] = band_ctry_qso_totals[bpos] + 1
                    band_qso_totals[bpos] = (
                        band_qso_totals[bpos]
                        + self.Countries_Band_To_Work[c][b]["status"]
                    )

            bpos = bpos + 1
        import pprint

        pprint.pprint(band_ctry_qso_totals)
        pprint.pprint(band_qso_totals)
        rv = "Band\tCtry\tTotal\n\n"
        for n in range(len(band_qso_totals)):
            rv = rv + "{}\t{}\t{}\t\n".format(
                self.hb.Band[n], band_ctry_qso_totals[n], band_qso_totals[n]
            )
        rv = rv + "\n\nLast Hours:\n\t\t1h {} 2h {} 4h {}".format(
            last_1_hour, last_2_hour, last_4_hour
        )
        return rv


if __name__ == "__main__":
    cc = ContestCountries()
    data = cc.process("General.csv")
    junk = 1
    print("" + data)
