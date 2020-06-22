from ham.mode.wsjx import LogRead
from ham.log import set_logging

if __name__ == "__main__":
    logger = set_logging()
    lr = LogRead(my_qra="PK05je")
    lr.dump_geo_to_file()
    print("Wsjk log file has been processed.")
