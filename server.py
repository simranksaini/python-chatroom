import socket
import threading


clients={}
addresses={}

BUFSIZ=1024 #Buffer size of the message being transmitted
PORT=33000  #Port number across which the communication is to happen
HOST=socket.gethostbyname(socket.gethostname()) #The ip address of the device
ADDR=(HOST,PORT) #A tuple of the ip address and the port number
FORMAT='utf-8' #Encoding/Decoding format for the message to be transmitted as
DISCONNECT_MSG="!DISCONNECT" #Disconnection message for the client

# Creating a socket at the server side, and binding it with the specified address
SERVER=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
SERVER.bind(ADDR)

def accept_connections():
    while True:
        #To accept the connection
        client,client_addr=SERVER.accept()

        #Log the connection details on the server side
        print(f"[NEW CONNECTION] {client_addr} connected.")

        #Welcoming the client.
        client.send(bytes("Hello!"+"Please type in your name and press enter.",FORMAT))

        #Adding the client address to the addresses dictionary for future use
        addresses[client]=client_addr

        #Creating a new thread for the specific client
        thread=threading.Thread(target=handle_client, args=(client,))
        #Starting the new thread
        thread.start()

def handle_client(client):
    #Receive the name of the client and decode it using the specified format
    name=client.recv(BUFSIZ).decode(FORMAT)

    #Send a welcoming message to the client and instructions on how to quit the chatroom
    welcome=f"Welcome {name}, If you ever want to quit, type "+DISCONNECT_MSG+" for a clean disconnection."
    client.send(bytes(welcome,FORMAT))

    #Broadcast the message to the already connected clients that we have a new connection.
    msg=f"{name} has joined the chatroom!"
    broadcast(bytes(msg,FORMAT))

    #Add the new client to the clients dictionary
    clients[client]=name

    #Infinite loop, waiting for the client's messages to broadcast. The loop will end once the client sends the disconnection message
    while True:
        #Receive any incoming message from a client
        clmsg=client.recv(BUFSIZ)

        #As long as the client does not send the disconnection message, broadcast it to the other connected clients.
        if clmsg!=bytes(DISCONNECT_MSG,FORMAT):
            broadcast(clmsg,name+": ")
    
        #If the client sends the disconnection message, close that connection, delete the client form the clients dictionary, notify other active clients that the specific client has disconnected, and break the while loop
        else:
            client.close()
            del clients[client]
            broadcast(bytes(f"{name} has left the chatroom!",FORMAT))
            break

#Broadcast the message to all the clients in the clients dictionary
def broadcast(msg,prefix=""):
    for sock in clients:
        sock.send(bytes(prefix,FORMAT)+msg)


if __name__=="__main__":
    SERVER.listen(5)
    print("Waiting for connection... ")
    ACCEPT_THREAD=threading.Thread(target=accept_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()