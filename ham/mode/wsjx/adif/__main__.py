from ham.mode.wsjx import LogRead
from ham.log import set_logging

if __name__ == "__main__":
    logger = set_logging()
    lr = LogRead(my_qra="PK05je")
    lr.dump_wsjx_to_adif()
    print("Wsjk log file has been processed into ADIF")
