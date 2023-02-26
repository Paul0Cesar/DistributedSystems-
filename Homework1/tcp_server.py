import socket
import sys
from threading import Thread, Lock
import os
from io import BytesIO


cache_lock = Lock()
global cache
global memory_cache_count
cache = dict()
memory_cache_count = 0
BUFFER_SIZE = 4096  # Byte ->4kb
TOTAL_CACHE_MEMORY = 64  # Megabytes
BYTE_TO_MB = 10**(-6)


def get_file_from_cache(file_name):
    '''Take the file name passed in the cache'''
    global cache
    cache_lock.acquire()
    hit = file_name in cache
    file = None
    if hit:
        file = cache[file_name]["file"]
    cache_lock.release()
    return file


def send_cache_list(connection):
    '''Send the passed all cache files names to the client'''
    global cache
    cache_lock.acquire()
    cache_list = "\n".join(list(cache.keys()))
    cache_lock.release()
    connection.sendall(cache_list.encode())


def update_cache(root_path, file_name, file):
    '''Update the cache with the passed file'''
    path = root_path+file_name
    global memory_cache_count
    global cache
    file_size = os.path.getsize(path)
    file_size = file_size*BYTE_TO_MB
    cache_lock.acquire()
    if file_size <= TOTAL_CACHE_MEMORY:
        if (TOTAL_CACHE_MEMORY-memory_cache_count) > file_size:
            cache[file_name] = {"file_name":file_name,"file":file.read(), "size": file_size}
            memory_cache_count = memory_cache_count+file_size
        else:
            for key,item in cache.copy().items():
                del cache[key]
                memory_cache_count = memory_cache_count-item["size"]
                if (TOTAL_CACHE_MEMORY-memory_cache_count) > file_size:
                    cache[file_name] = {"file_name":file_name,"file": file.read(), "size": file_size}
                    memory_cache_count = memory_cache_count+file_size
                    break
    cache_lock.release()


def send_file(connection, file):
    '''Send the passed file to the client passed'''
    if isinstance(file,bytes):
        file = BytesIO(file)
    while True:
        bytes_read = file.read(BUFFER_SIZE)
        if not bytes_read:
            break
        connection.sendall(bytes_read)


def new_connection(connection, client_address, root_path):
    '''Create a new connection by client'''
    try:
        print(f"Connected by {client_address}")
        file_name = connection.recv(BUFFER_SIZE).decode()
        if file_name:
            if (file_name == "list"):
                send_cache_list(connection)
            else:
                print(
                    f"Client {client_address} is requesting file {file_name}")
                file = get_file_from_cache(file_name)
                if file is not None:
                    print(f"Cache hit. File {file_name} sent to the client.")
                    send_file(connection, file)
                else:
                    path = root_path+file_name
                    if os.path.isfile(path):
                        print(f"Cache miss. File {file_name} sent to the client")
                        with open(path, "rb") as file:
                            update_cache(root_path, file_name, file)
                            file.seek(0)
                            send_file(connection, file)
                    else:
                        print(f"File {file_name} does not exist")
    finally:
        connection.close()


def run():
    '''Start'''
    port = int(sys.argv[1])
    root_path = sys.argv[2]
    print("port:", port, " Root Path:", root_path)
    service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    service.bind(("127.0.0.1", port))
    service.listen()
    while True:
        print("waiting for a connection...")
        connection, client_address = service.accept()
        Thread(name=f"Thread-{client_address[1]}",
               target=new_connection, args=(connection, client_address, root_path)).start()


run()
