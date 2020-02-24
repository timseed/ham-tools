from ham.mode.wsjx import LogRead

if __name__ == "__main__":
    lr = LogRead(my_qra="PK05je")
    lr.dump_geo_to_file()
    print("Wsjk log file has been processed.")
