import socket
import select
import sys

ECHO_PORT = 9999
BUF_SIZE = 4096

def main():
    print("----- Echo Server -----")
    try:
        serverSock = socket.socket()
    except socket.error as err:
        print ("socket creation failed with error %s" %(err))
        exit(1)
    serverSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    serverSock.bind(('0.0.0.0', ECHO_PORT))
    serverSock.listen(5)
    serverSock.setblocking(0)
    epoll = select.epoll()
    epoll.register(serverSock.fileno(), select.EPOLLIN)

    connections = {} #stores all the socket connections
    data_queue = {} #stores the data to be sent back to the clients


    while True:

   
        events = epoll.poll(0); #non blocking poll, poll immediately and can be empty 
       
        for file_desc, event in events:
            #new connections for incoming clients
         
            if (file_desc == serverSock.fileno()):
                try:
                    while True:
                        client_soc, client_addr = serverSock.accept()
                        client_soc.setblocking(0)
                        client_file_desc = client_soc.fileno()
                        connections[client_file_desc]= client_soc
                        data_queue[client_file_desc]= b''
                        epoll.register(client_file_desc, select.EPOLLIN);
                except BlockingIOError: #no more connections 
                    pass
            elif (event & select.EPOLLIN): #incoming data from a client 
                try:

                    while True: #keep reading data until data is empty, indicateing client is done sending

                        data = connections[file_desc].recv(BUF_SIZE)
                        if (data):
                            data_queue[file_desc] += data;

                            epoll.modify(file_desc,select.EPOLLOUT) #send data back to client the following epoll.poll(), this can be outside the if statement, but won't change functionality
                        else:
                            epoll.unregister(file_desc)
                            connections[file_desc].close()
                            del connections[file_desc]
                            del data_queue[file_desc]
                            break
                except BlockingIOError: #no more data to read, CURRENTLY

                    pass
                except ConnectionResetError: #handling if connection ends abruptly. shut down connection
                    epoll.unregister(file_desc);
                    connections[file_desc].close()
                    del connections[file_desc]
                    del data_queue[file_desc]
            elif (event & select.EPOLLOUT): #sending data back to client
                if (data_queue[file_desc]): #if there is data to send

                    try:
                        sent = connections[file_desc].send(data_queue[file_desc])
                        data_queue[file_desc] = data_queue[file_desc][sent:]

                        if (not data_queue[file_desc]):
                            epoll.modify(file_desc, select.EPOLLIN)
                    except BlockingIOError: #socket not ready to send, try again later
                        pass
                    except ConnectionResetError: #handling if connection ends abruptly. shut down connection
                        epoll.unregister(file_desc);
                        connections[file_desc].close();
                        del connections[file_desc]
                        del data_queue[file_desc];
                else:
                    epoll.modify(file_desc,select.EPOLLIN) #no more data to send, go back to reading in data. technically this case shouldn't happen, since every epoll out is preceeded by data being added to the queue via epollin. this can allow the changing of line 42 to be epollout or epollin
                   

                   
               

if __name__ == '__main__':
    main()