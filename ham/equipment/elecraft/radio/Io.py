import serial
import daiquiri


class Io:
    def __init__(self):

        self.ser = None
        self.logger = daiquiri.getLogger(__name__)

    def open_serial(
        self, device="/dev/cu.usbserial-A7004VW8", baud_rate=38400, timeout=1
    ):
        """
        Open the serial Device
        :param device:
        :param baud_rate:
        :param timeout:
        :return:
        """
        return serial.Serial(device=device, baudrate=baud_rate, timeout=1)

    def show_port(self) -> str:
        """
        Return a string descripbing the connected port
        :return: str
        """

        if self.ser:
            return f"{self.ser.port}"
        else:
            return None

    def close(self):
        """
        Close connection to the radio.
        :return:
        """
        self.ser.flushInput()  # until the "quit" comes along.
        self.ser.close()

    def write(self, str_command: str) -> None:
        """
        Generic routine to send a command string - to the radio.

        Please note the data need to be binary encoded before it can be sent.

        :param str_command: Command string(s) i.e. K22;MD
        :return: None
        """
        str_command=str_command.rstrip(';')

        for a in str_command.split(";"):
            self.logger.debug("Sending Data to Serial Port")
            self.ser.write((a + ";").encode("utf-8"))
            # self.ser.flushInput()

    def read(self, bytes_to_read: int) -> str:
        """
        Generic read routine.
        needs to know how many bytes to read.

        :param bytes_to_read: Number of bytes
        :return: a UTF-8 String of the returned data.
        """
        try:
            return self.ser.read(bytes_to_read).decode("utf-8")
        except:
            self.logger.error("Error Reading data")
            return ""
