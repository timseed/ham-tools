# Echo client program
import socket, select
import sys


class telnet(object):
    def __init__(self):
        HOST = "gb7mbc.spoo.org"  # The remote host
        PORT = 8000  # The same port as used by the server
        s = None

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = socket.gethostbyname(HOST)
        self.s.connect((addr, PORT))
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

    def SendData(self, utf_str):
        datab = utf_str.encode("utf-8")
        self.s.sendall(datab)

    def GetData(self):
        data = self.s.recv(1024)
        # print('Received', repr(data))
        ds = data.decode("utf-8")
        return ds


if __name__ == "__main__":
    tnc = telnet()
    print("done")

# gb7mbc.spoo.org
