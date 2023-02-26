import socket
import sys
import os


BUFFER_SIZE = 4096

HOST = sys.argv[1]
PORT = int(sys.argv[2])
FILE = sys.argv[3]
PATH_TO_SAVE = ''
if len(sys.argv)>4:
    PATH_TO_SAVE = sys.argv[4] 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))
client.send(FILE.encode())
path=PATH_TO_SAVE+FILE
is_valid=False

if FILE=="list":
    bytes_read = client.recv(BUFFER_SIZE)
    print(bytes_read.decode())
else:
    try:
        with open(path, "wb") as f:
            while True:
                bytes_read = client.recv(BUFFER_SIZE)
                if not bytes_read:    
                    break
                is_valid=True
                f.write(bytes_read)
    finally:
        if not is_valid:
            os.remove(path)
    if is_valid:
        print(f"File {FILE} saved")
    else:
        print(f"File {FILE} does not exist in the server.")