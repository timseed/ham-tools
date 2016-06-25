

import csv


class csv2adif(object):

    def __init__(self,filename):
        self.filename=filename

    def process(self):
        with open(self.filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                line=''
                for fld in reader.fieldnames:
                    if len(row[fld].strip()) > 0:
                        line = line+str.format("<{}:{}>{} ",fld,len(row[fld].strip()),row[fld].strip())

                yield(line + " <eor>")
        csvfile.close()


if __name__ == "__main__":
    cvt = csv2adif("asian2016.csv")
    for a in cvt.process():
        print('' + a)
