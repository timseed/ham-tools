from mock_pyserial.mock_serial import Serial as mock_serial


class NonArduinoSerial(mock_serial):
    """
    The default Python mock_serial is for Arduino. And only accepts UTF data.
    The K3 sends data as Binary.
    """

    def __init__(
        self,
        port="COM1",
        baudrate=19200,
        timeout=1,
        bytesize=8,
        parity="N",
        stopbits=1,
        xonxoff=0,
        rtscts=0,
    ):
        self.name = port
        self.port = port
        self.timeout = timeout
        self.parity = parity
        self.baudrate = baudrate
        self.bytesize = bytesize
        self.stopbits = stopbits
        self.xonxoff = xonxoff
        self.rtscts = rtscts
        self._isOpen = True
        self._receivedData = b""
        self._data = "It was the best of times.\nIt was the worst of times.\n"

    def write(self, string):
        self._receivedData += b"{string}"

    def flushInput(self):
        self._receivedData = b""

    def flushOutput(self):
        self._data = b""
