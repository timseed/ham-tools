# Echo client program
import socket, select
import sys


class Telnet(object):
    def __init__(self):
        host = "gb7mbc.spoo.org"  # The remote host
        port = 8000  # The same port as used by the server
        s = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.gethostbyname(host)
        self.s.connect((addr, port))
        while 1:
            socket_list = [sys.stdin, self.s]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(
                socket_list, [], []
            )

            for sock in read_sockets:
                # incoming message from remote server
                if sock == s:
                    data = sock.recv(4096)
                    if not data:
                        print("Connection closed")
                        sys.exit()
                    else:
                        # print data
                        sys.stdout.write(data)

                # user entered a message
                else:
                    msg = sys.stdin.readline()
                    s.send(msg)

    def senddata(self, utf_str):
        datab = utf_str.encode("utf-8")
        self.s.sendall(datab)

    def getdata(self):
        data = self.s.recv(1024)
        # print('Received', repr(data))
        ds = data.decode("utf-8")
        return ds
