from ham.mode.wsjx import LogRead

if __name__ == "__main__":
    lr = LogRead(my_qra="PK05je")
    lr.dump_wsjx_to_adif()
    print("Wsjk log file has been processed into ADIF")
