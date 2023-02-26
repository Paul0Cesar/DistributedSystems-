# Distributed Systems - Homework 1 :computer:

## How it works? :robot:

The server module is responsible for waiting for client connections and using the argument passed to find the file in the path designated, and send this file to the client. At the first moment, the file is not present in the cache and the server needs to save then after the service can get the same file now in the cache instead find the file in the operational system.

The client module is responsible for sending the argument (file name) to the server module, and if the result is positive, the client saves the file received.


Running the server: 

```shell
python tcp_server.py PORT PATH_OF_FILES
```

Running the client:

```shell
python tcp_client.py SERVER_IP SERVER_PORT FILE_NAME PATJ_TO_SAVE_FILES
```

## Architecture :books::

The server is made using the single responsibility principle by function. Where the function is responsible for one functionality specific. This way, it is easier for the reader to understand and easier for the maintainer.

If you look nearer, the system has a similarity with endpoints, where, depending on the argument passed by the client, one function is selected.

## Technologies and Challenges :mag_right: :chart_with_upwards_trend:: 

The protocol selected is Transmission Control Protocol (TCP) using the address family IPV4. the TCP is required because we want to ensure the receive of the data.

```python3
    service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
```

> **Explaining the Arguments:** \
>AF_INET => Select the IPV4 family 
>
>SOCK_STREA =>  Socket type TCP


The system is made to receive multi connections, therefore the system is multi-thread. For this we use threading, a native lib present in python, for creating parallel processes by clients.

The line below, shows when the connection is received in the service, the server creates a new thread : 

```python3
        connection, client_address = service.accept()
        Thread(name=f"Thread-{client_address[1]}",
               target=new_connection, args=(connection, client_address, root_path)).start()
```

The server is made with a cache in memory, using the dictionary to store the data and facility the get for send for the client. Using global operator, present in python to share the same variable with all threads. But with this operator, we gain some challenge, the concurrency, and for solving this problem we use Look, class present in threading lib, to lock the use of this variable, and show it to other threads to wait for the release for use.
