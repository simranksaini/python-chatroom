import socket
import threading
import time


BUFSIZ = 1024 #Buffer size of the message being transmitted
PORT = 33000  #Port number across which the communication is to happen (should be same as the server's)

# The ip address of the device
HOST = socket.gethostbyname(socket.gethostname())
#A tuple of the ip address and the port number
ADDR = (HOST, PORT)
#Encoding/Decoding format for the message to be transmitted as
FORMAT = 'utf-8'
#Disconnection message for the client
DISCONNECT_MSG = "!DISCONNECT"

# Creating a socket at the client side, and connecting it to the server with the specified address
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(ADDR)

def receive():
    #Infinite loop that receive messages from the server until the client leaves the chat
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode(FORMAT)
            print(msg)
        except OSError: 
            break

def send():
    #Input and send the username to the server
    my_username = input("")
    username = my_username.encode(FORMAT)
    client_socket.send(username)

    #An infinite loop that will send the client's messages to the server, it will end once the client enters the disconnection message
    while True:
        msg=input(f"")
        #Unless the message is not a disconnection message, it will be encoded and sent to the server
        if msg!=DISCONNECT_MSG:
            msg=msg.encode(FORMAT)
            client_socket.send(msg)
        #If the message is the disconnection message, It will notify the server, close the socket connection, and break out of the while loop
        else:
            msg = msg.encode(FORMAT)
            client_socket.send(msg)
            client_socket.close()
            break

def main():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    send_thread = threading.Thread(target=send)
    send_thread.start()

    time.sleep(1)
    while threading.activeCount() > 1:
        pass


if __name__ == '__main__':
    main()
