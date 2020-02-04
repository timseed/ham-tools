import telnetlib
import logging


class Telnet3(telnetlib.Telnet):
    def read_until(self, expected, timeout=None):
        """

        :param expected:
        :param timeout:
        :return:
        """
        expected = bytes(expected, encoding="utf-8")
        received = super(Telnet3, self).read_until(expected, timeout)
        logging.info("read_util length =" + str(len(received)))
        logging.info("data=>" + str(received, encoding="utf-8"))
        return str(received, encoding="utf-8")

    def write(self, buffer):
        """

        :param buffer:
        :return:
        """
        logging.info("write data =>" + buffer + "<=")
        buffer = bytes(buffer, encoding="utf-8")
        super(Telnet3, self).write(buffer)

    def expect(self, list, timeout=None):
        """

        :param list:
        :param timeout:
        :return:
        """
        for index, item in enumerate(list):
            list[index] = bytes(item, encoding="utf-8")
        match_index, match_object, match_text = super(Telnet3, self).expect(
            list, timeout
        )
        return match_index, match_object, str(match_text, encoding="utf-8")
