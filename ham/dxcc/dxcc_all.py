import logging
import os
import re
import ham.dxcc
from ham.dxcc.dxobj import DxObj
from typing import Optional


class DxccAll(object):
    """

    """

    def __init__(self):
        """

        """
        self._dxcc_list = {}
        self.logger = logging.getLogger(__name__)
        formatter = logging.Formatter(
            "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
            "%m-%d %H:%M:%S",
        )
        self.read()

    # TODO this needs writing
    def removewae(self) -> bool:
        """
        Some prefixes exist only for WAE
        :return:
        """
        return True

    def correctdata(self, prefix: str, dx_rec: list):
        """
        (#)	Override CQ Zone
        [#]	Override ITU Zone
        <#/#>	Override latitude/longitude
        {aa}	Override Continent
        ~#~	Override local time offset from GMT

        i.e. YG0[54] means Override the ITU Zone

        :param prefix:
        :rtype: object
        :param dx_rec:
        :return: prefix, DxRec
        """

        prefix = prefix.replace(" ", "")
        m = re.search("[^A-Za-z0-9]", prefix)
        if m is not None:
            if prefix.startswith("="):
                self.logger.debug("Specific Call")
                prefix = prefix.replace("=", "")
            m_cq = re.search("([(][0-9]+[)])", prefix)
            if m_cq is not None:
                # CQ Zone Change
                new_cq_zone = m_cq.groups(0)[0]
                self.logger(str.format("{} has CQZone Change {}", prefix, new_cq_zone))
                prefix = prefix.replace(new_cq_zone, "")
                new_cq_zone = new_cq_zone.replace("(", "").replace(")", "")
                # Make new tuple
                #
                x = (new_cq_zone,)
                dx_rec = dx_rec[:1] + x + dx_rec[2:]
            m_itu = re.search(r"(\[[0-9]+\])", prefix)
            if m_itu is not None:
                new_itu_zone = m_itu.groups(0)[0]
                self.logger.debug(
                    str.format("{} has ITU Change {}", prefix, new_itu_zone)
                )
                prefix = prefix.replace(new_itu_zone, "")
                new_itu_zone = new_itu_zone.replace("[", "").replace("]", "")
                # Make new tuple
                #
                x = str(new_itu_zone,)
                dx_rec = dx_rec[:2] + x + dx_rec[3:]
            m_cont = re.search(r"({[0-9]+})", prefix)
            if m_cont is not None:
                new_cont = str(m_cont.groups(0)[0])
                self.logger.debug(str.format("{} has ITU Change {}", prefix, new_cont))
                prefix = prefix.replace(new_cont, "")
                new_cont = new_cont.replace("{", "").replace("}", "")
                # Make new tuple
                #
                x = str(new_cont,)
                dx_rec = dx_rec[:3] + x + dx_rec[4:]

        return prefix, dx_rec

    def read(self) -> int:
        """
        Read the cty.dat file which is embedded in the project.

        :return: Number of DXCC Entries
        """
        self._dxcc_list = {}
        wanted_file = ""
        try:
            wanted_file = (
                os.path.join(os.path.dirname(ham.dxcc.__file__), "data") + "/cty.dat"
            )
            logging.debug(f"want to open {wanted_file}")
            print(f"want to open {wanted_file}")
            txt = open(wanted_file).read()
            logging.debug("file opened")
            element = txt.split(";")
            for e in element:
                if len(e) > 10:  # Min string size
                    try:
                        parts = tuple(
                            [
                                a.rstrip(" ").lstrip(" ").replace("\n", "")
                                for a in e.split(":")
                            ]
                        )
                        prefix = str(parts[8]).rstrip(" ").lstrip(" ")
                        for p in prefix.split(","):
                            try:
                                tmp_parts = parts[0:7]
                                clean_prefix, tmp_parts_2 = self.correctdata(
                                    p, tmp_parts
                                )
                                d = DxObj(
                                    call_starts=clean_prefix,
                                    country_name=tmp_parts_2[0],
                                    cq_zone=tmp_parts_2[1],
                                    itu_zone=tmp_parts_2[2],
                                    continent_abbreviation=tmp_parts_2[3],
                                    latitude=float(tmp_parts_2[4]),
                                    longitude=float(tmp_parts_2[5]),
                                    local_time_offset=float(tmp_parts_2[6]),
                                )

                                self._dxcc_list[clean_prefix] = d
                                # self.logger.debug("Array has ", str(len(self._dxcc_list)))
                            except IndexError:
                                self.logger.debug("Index Error" + e)
                                pass
                            except Exception as un_err:
                                self.logger.debug("Some other error: " + str(un_err))
                    except IndexError as ie:
                        self.logger.error(f"Outer Index Error {str(ie)}")
                        pass
                    except Exception as er:
                        self.logger.error(f"Outer Some other error {str(er)}")
        except NameError as ne:
            self.logger.error(f"File Opening {wanted_file} {str(ne)} Error")
            exit(1)

        except Exception as err:
            self.logger.error(f"{str(err)} Some other error has occurred")
            pass
        return len(self._dxcc_list)

    def show(self, dx_station):

        for dx in self._dxcc_list:
            if dx_station.startswith(dx):
                self._dxcc_list[dx].show()
                return self._dxcc_list[dx]
        return None

    def showall(self) -> None:
        for a in sorted(self._dxcc_list):
            self._dxcc_list[a].show()

    # TODO This needs completing
    def std_call(self, call: str) -> Optional[str]:
        """
        try and fix a callsign that can be entered like this du2/m0fgc/p or m0fgc/du2 or m0fgc/p
        Is
            * English Call
            * In Philippines

        :param call:
        :return:

        """
        cs = "/".join(sorted(call.upper().split("/"), key=len, reverse=True))

        cnt = cs.count("/")
        if cnt == 0:
            # No /'s
            return cs
        elif cnt == 1:
            # m0fgc/p or du2/m0fgc
            # EEK
            help = 1
            return None

    def find(self, call: str) -> DxObj:
        """
        Find the Country to a call sign
        Get all prefixes - sort by the length of the string - and then iterate LONGEST prefix first.


        :param call: Full or Partial Call
        :return: Matched DXCC Entity - None if not Found

        """
        match = None
        prefix = [a for a in self._dxcc_list]
        prefix.sort(key=len)
        for n in prefix[::-1]:
            if call.startswith(n):
                match = self._dxcc_list[n]
                break
        return match

    @property
    def prefix(self) -> list:
        """
        A list of all the Prefixes  - not ordered or sorted.
        :return: list
        """
        return [a for a in self._dxcc_list]

    @property
    def countrylist(self) -> list:
        """
        List of all Countries (not Prefixes) i.e. DU1,DU2,DU3 are just 1 Country.
        :return: List of All Country Names
        """
        countrynames = list(set([self._dxcc_list[k].Country_Name for k in self._dxcc_list.keys()]))
        countrynames.sort()
        return countrynames
