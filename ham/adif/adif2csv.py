import re
from collections import OrderedDict

"""
Simple class to take adif file - and create csv
"""


class Adif2Csv(object):
    """
    adiftocsv. This version assumes that all Columns are filled in the same.

    expected usage
    import adif2csv
    cvt=adif2csv()
    cvt.process("test.adif")
    for a in cvt.dump():
        print(''+a,end='')
    """

    def __init__(self, all_lines_same=False):
        """
        Basic constructor
        :return:  None
        """
        # self.fields = {}
        self.lines = []
        self.header = ""
        self.all_lines_same = all_lines_same

    def process(self, filename):
        """
        Open the file and store the data internally

        Note: At the moment there is no error checking that this has worked.

        :type all_lines_same:
        :param filename:
         :return:
        """
        with open(filename, "rt") as f:
            for line in f:
                if line.startswith("<call"):
                    self.lines.append(line)
            f.close()
        self.make_dict()

    def make_dict(self):
        """
        This gnerates the header for the CSV file
        :param all_lines_same:
        :return:
        """
        if self.all_lines_same:
            if len(self.lines) > 0:

                """
                Make a regex to find the adif_codes, then chop the 1st letter off the string.
                Finally stitch it together as a string - and we have the header
                """
                self.header = ",".join(
                    [a[1:] for a in re.findall(r"<[a-z_]+", self.lines[0])]
                )
            else:
                print("Error No dictionary can be made - there is no data")
        else:
            head = []
            """
            Need to read
            Every line and place the tags into an array
            """
            for l in self.lines:
                tmp = [a[1:] for a in re.findall(r"<[a-z_]+", l)]
                head = head + tmp
                # Do this to keep the list small
                head = list(set(head))

            # Get the Unique tags
            unique_head = head
            self.header = ",".join([a for a in unique_head])

    def dump(self):
        """
        Simple iterator to allow the converted data to be output
        :return:
        """
        if self.all_lines_same:
            yield "" + self.header + "\n"
            for line in self.lines:
                """
                The data looks like this when split using <

                [
                '',
                'call:4>LZ7M ',
                'qso_date:8>20160618 ',
                ]

                So we split again using > - but only for an object who's length is > 0
                """
                yield (
                    ",".join(
                        [f.split(">")[1].strip() for f in line.split("<") if len(f) > 0]
                    )
                    + "\n"
                )
        else:
            """
            We have a Variable format input - but we need to create a fixed output.
            """
            line_count = 0
            for line in self.lines:
                # Create a Blank Dictionary
                out_dict = {}
                # Fill every field based on the headers we saw
                for k in self.header.split(","):
                    out_dict[k] = ""

                if line_count == 0:
                    line_count = line_count + 1
                    od = OrderedDict(sorted(out_dict.items()))
                    out = ""
                    for k, v in od.items():
                        out = out + str.format("{},", k)
                    yield out + "\n"

                """
                Parse the Line - filling in the dictionary as we go
                """
                parts = [a for a in line.split("<") if len(a) > 0]
                """
                Each record now looks like this
                'srx_string:2>68 ',
                'freq:8>7.024380  ',
                """
                for p in parts:
                    pp = p.split(":")
                    if len(pp) == 2:
                        k = pp[0]
                        d = pp[1]
                        if k in out_dict:
                            data = d.split(">")[1]
                            out_dict[k] = data
                        else:
                            print(
                                str.format("Error as {} is not in output dictionary", k)
                            )
                    else:
                        # it should be the EOR field
                        junk = 1

                """
                At this point we should have processed the line
                In case the dictionary changes the output order
                we will use an ordered dictionary
                """
                od = OrderedDict(sorted(out_dict.items()))
                out = ""
                for k, v in od.items():
                    out = out + str.format("{},", v)
                yield out + "\n"
