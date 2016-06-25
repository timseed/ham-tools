import re
import pprint
import pkg_resources



class dxcc(object):
    def __init__(self):
        self._dxcc = {}

    def RemoveWAE(self):
        """
        Some prefixes exist only for WAE
        Not yet implemented
        :return:
        """

    def correctdata(self, prefix, DxRec):
        """
        (#)	Override CQ Zone
        [#]	Override ITU Zone
        <#/#>	Override latitude/longitude
        {aa}	Override Continent
        ~#~	Override local time offset from GMT

        i.e. YG0[54] means Override the ITU Zone

        :rtype: object
        :param DxRec:
        :return: prefix, DxRec
        """

        prefix = prefix.replace(' ', '')
        m = re.search('[^A-Za-z0-9]', prefix)
        if m != None:
            # print("Prefix is Special "+prefix)
            if prefix.startswith('='):
                print("Specific Call")
                prefix = prefix.replace('=', '')
            mCQ = re.search('(\([0-9]+\))', prefix)
            if mCQ != None:
                # CQ Zone Change
                newCqZone = mCQ.groups(0)[0]
                print(str.format("{} has CQZone Change {}", prefix, newCqZone))
                prefix = prefix.replace(newCqZone, '')
                newCqZone = newCqZone.replace('(', '').replace(')', '')
                # Make new tuple
                #
                x = (newCqZone,)
                DxRec = (DxRec[:1] + x + DxRec[2:])
            mITU = re.search('(\[[0-9]+\])', prefix)
            if mITU != None:
                newITUZone = mITU.groups(0)[0]
                print(str.format("{} has ITU Change {}", prefix, newITUZone))
                prefix = prefix.replace(newITUZone, '')
                newITUZone = newITUZone.replace('[', '').replace(']', '')
                # Make new tuple
                #
                x = (newITUZone,)
                DxRec = (DxRec[:2] + x + DxRec[3:])
            mCONT = re.search('({[0-9]+})', prefix)
            if mCONT != None:
                newCont = mCONT.groups(0)[0]
                print(str.format("{} has ITU Change {}", prefix, newCont))
                prefix = prefix.replace(newCont, '')
                newCont = newCont.replace('{', '').replace('}', '')
                # Make new tuple
                #
                x = (newCont,)
                DxRec = (DxRec[:3] + x + DxRec[4:])

        return prefix, DxRec

    def read(self):
        self._dxcc = {}
        try:
            file = pkg_resources.resource_filename(__name__, "cty.dat")
            txt = open(file).read()
            element = txt.split(';')
            for e in element:
                if len(e) > 0:
                    try:
                        parts = tuple([a.rstrip(' ').lstrip(' ').replace('\n', '') for a in e.split(':')])
                        prefix = str(parts[8]).rstrip(' ').lstrip(' ')

                        for p in prefix.split(','):
                            try:
                                tmp_parts = parts[0:7]
                                clean_prefix, tmp_parts_2 = self.correctdata(p, tmp_parts)

                                self._dxcc[clean_prefix] = tmp_parts_2
                                print("Array has ", str(len(self._dxcc)))
                            except IndexError:
                                print("Error" + e)
                                pass
                            except:
                                print("Some other error")
                    except IndexError:
                        print("Error" + e)
                        pass
                    except:
                        print("Some other error")
        except:
            print("File Opening Error" + file)
            exit(1)

        pprint.pprint(self._dxcc)

    def show(self, dx_station):

        for dx in self._dxcc:
            if dx_station.startswith(dx):
                print(str.format(
                    'Country {}:\n\tCQ\t{}\n\tITU\t{}\n\tAbbv\t{}\n\t\tPos\n\t\t\tLat\t{}\n\t\t\tLon\t{}\n\tTZ\t{}',
                    self._dxcc[dx][0], self._dxcc[dx][1],
                    self._dxcc[dx][2], self._dxcc[dx][3], self._dxcc[dx][4], self._dxcc[dx][5], self._dxcc[dx][6]))
                # else:
                #    print("Error "+dx+" Not found")

    def showall(self):
        for a in sorted(self._dxcc):
            print(str.format("Prefix {} {} ", a, self._dxcc[a][0]))
        pprint.pprint(self._dxcc['DU'])

    def std_call(self, call):
        """
        try and fix a callsign that can be entered like this du2/m0fgc/p or m0fgc/du2 or m0fgc/p
        Is
            * English Call
            * In Philippines

        :param call:
        :return:

        """
        cs = '/'.join(sorted(call.upper().split('/'), key=len, reverse=True))

        cnt = cs.count('/')
        if cnt == 0:
            # No /'s
            return cs
        elif cnt == 1:
            # m0fgc/p or du2/m0fgc
            # EEK
            help = 1

    def find(self, call):
        """
        Find the Country to a call sign

        :param call: Full or Partial Call
        :return: Matched DXCC Entity - None if not Found

        """
        match = None
        for a in sorted(self._dxcc):
            if str(self._dxcc[a]).startswith(call):
                match = self._dxcc[a]
                break
        return match


if __name__ == "__main__":
    d = dxcc()
    d.read()
    d.showall()
    # d.show('G')
    # d.show('F')
    d.show('M0FGC')
