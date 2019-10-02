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
        self.filename_buffer = ''
        self.final_filename = ''
        self.filedata_buffer = b''

    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        if not self.filename_known:

            name_data = self.sock.recv(1024)

            if name_data:
                # write filename to temporary buffer

                self.filename_buffer += name_data.decode()
            else:

                self.filename_known = True
                print('Filename is ' + self.filename_buffer)
            
                if self.filename_buffer in files:

                    print('Collision occured!')
                    i = len(self.filename_buffer) - 1

                    while not self.filename_buffer[i] == '.':
                        if i == 0:
                            break
                        i -= 1
                    
                    file_name = ''
                    file_extension = ''
                    
                    if i == 0:
                        file_name = self.filename_buffer
                        file_extension = ''
                    else:
                        file_name = self.filename_buffer[:i]
                        file_extension = self.filename_buffer[i:]

                    copy_num = 1

                    while not file_name + '_copy' + str(copy_num) + file_extension in files:
                        copy_num += 1

                    self.final_filename = file_name + '_copy' + str(copy_num) + file_extension

                    files.append(self.final_filename)
                    print('New file name is ' + self.final_filename)
                else:

                    print('No collision occured.')
                    files.append(self.filename_buffer)
        else:
            # send 'accept' message to the client and wait for the file

            accept_data = 'filename_accepted'.encode()
            for u in clients:
                if u == self.sock:
                    u.sendall(accept_data)   

            file_data = self.sock.recv(1024)
            
            if file_data:
                self.filedata_buffer += file_data
            else:
                f = open(self.final_filename, 'wb+')
                f.write(self.filedata_buffer)
                f.close()
                print('File ' + self.final_filename + ' was received.')
                self._close()
                return

def main():

    print('Server is ready for users')

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

