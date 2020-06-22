from ham.mode.ft8 import LogRead
from ham.log import set_logging

if __name__ == "__main__":
    logger  = set_logging()
    lr = LogRead(my_qra="PK05je")
    lr.dump_geojson_to_file()
    lr.dump_data_to_pickle()
    print("ft8 log file has been processed.")
