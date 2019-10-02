import sys
import socket
from threading import Thread


files = []
clients = []


class ClientListener(Thread):
    def __init__(self, name: str, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name
        self.filename_known = False

    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        if not filename_known:
            filename_buffer = ''
            name_data = self.sock.recv(1024)
            if name_data:
                # write filename to temporary buffer

                filename_buffer += name_data.decode()
            else:
                filename_known = True
                print('Filename is ' + filename_buffer)
            
                if filename_buffer in files:
                    print('Collision occured!')
                    i = len(filename_buffer) - 1
                    while not filename_buffer[i] == '.':
                        i -= 1
                    file_name = filename_buffer[:i]
                    file_extension = filename_buffer[i:]
                    copy_num = 1
                    while not file_name + '_copy' + str(copy_num) + file_extension in files:
                        copy_num += 1
                    files.append(file_name + '_copy' + str(copy_num) + file_extension)
                else:
                    print('No collision occured.')
                    files.append(filename_buffer)
        else:
            # send 'accept' message to the client and wait for the file
            accept_data = 'filename_accepted'.encode()
            for u in clients:
                if u == self.sock:
                    u.sendall(accept_data)   

            file_data = self.sock.recv(1024)
            
            if file_data:
                # write to the file
            else:
                self._close()
                return

def main():
    next_name = 1

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()

    while True:
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        ClientListener(name, con).start()


if __name__ == '__main__':
    main()

