import os
import sys
import socket


def main():
    
    # Retrieve arguments from the command line  
    filename = sys.argv[1]
    ip = sys.argv[2]
    port = sys.argv[3]

    # Open given file
    f = open(filename, "rb")

    # Define socket for file transfer
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((ip, int(port)))
    
    # Send filename to the server
    send_data = filename + ('?' * (1024 - len(filename)))
    sock.sendall(filename.encode())
    
    # Wait until server is operating with filename
    print('Waiting for the response...')
    response = sock.recv(1)
    print('Response was received')

    # Get filesize for the progress bar
    old_file_position = f.tell()
    f.seek(0, os.SEEK_END)
    file_size = f.tell()
    f.seek(old_file_position, os.SEEK_SET) 

    # Transfer loop
    i = 1
    buff = b''
    while True:

        # Read next byte
        byte = f.read(1)
        
        # Break if EOF
        if byte == b'':
            sock.sendall(buff)
            break
        else:
            # Send group of 64 bytes and update progress bar
            if i % 64 == 0:
                
                hashtags = '#' * int((i / file_size) * 20)
                dots = '.' * (20 - len(hashtags))
                
                print('\033[F\033[K' + 'Progress: ' + hashtags + dots + ' ')

                buff += byte
                sock.sendall(buff)
                buff = b''
                i += 1
            else:
                buff += byte
                i += 1   
    
    print('The file has been sent')

    f.close()    


if __name__ == '__main__':
    main()

