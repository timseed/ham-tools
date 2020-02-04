import socket, select, sys
import logging
from datetime import datetime

__author__ = "timothyhseed"


class dxspider(object):
    def __init__(self, node: str, port: int, call: str) -> None:
        """

        :param node:
        :param port:
        :param call:
        """

        self.node = node
        self.port = port
        self.call = call
        self.s = None
        self.firsttime = True
        self.socket_list = []
        self.logger = logging.getLogger()
        print(str.format("logger Name is {}", self.logger.name))
        self.logger.info(str.format("Node is {}", node))
        self.logger.info(str.format("port is {}", port))
        self.logger.info(str.format("User is {}", call))

    def __del__(self):
        self.logger.info(str.format("destructor being called "))

    def do_connect(self):
        self.logger.info(str.format("Do_Connect"))
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logger.info(str.format("Socket created"))
        self.s.settimeout(2)

        # connect to remote host
        try:
            self.s.connect((self.node, int(self.port)))
        except Exception as err:
            print("Unable to connect " + str(err))
            return False
        print("Connected to remote host")
        return True

    def get_dx(self, msg_to_send=""):
        self.socket_list = [sys.stdin, self.s]

        # Get the list sockets which are readable

        read_sockets, write_sockets, error_sockets = select.select(
            self.socket_list, [], []
        )

        if self.firsttime is True:
            self.s.send(str(self.call + "\n").encode())
            self.firsttime = False

        for sock in read_sockets:
            # incoming message from remote server
            if sock == self.s:
                data = sock.recv(4096)
                if not data:
                    print("Connection closed")
                    sys.exit()
                else:
                    # print data
                    try:
                        nw = datetime.now()
                        sys.stdout.write(
                            str(nw.isoformat(sep=" ")) + "   " + data.decode("utf-8")
                        )
                    except:
                        junk = 1
                        pass

            # user entered a message
            else:
                if len(msg_to_send):
                    msg = sys.stdin.readline()
                    self.s.send(msg.encode())
