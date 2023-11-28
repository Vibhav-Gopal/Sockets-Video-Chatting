#importing libraries
import socket
import cv2
import pickle
import struct
import threading
# Server socket
# create an INET, STREAMing socket
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:',host_ip)
port = 10050
socket_address = (host_ip,port)
print('Socket created')

server_socket.bind(socket_address)
print('Socket bind complete')

server_socket.listen(5)
print('Socket now listening')

clients=dict()

def handle_client(client_socket):
    data = b""
    while True:
        try: 
            payload_size = struct.calcsize("Q")
            while len(data)<payload_size:
                packet = client_socket.recv(1)
                if not packet : break
                data+=packet
            packedSize = data[:payload_size]
            data = data[payload_size:]
            msgSize = struct.unpack("Q",packedSize)[0]
            while len(data) < msgSize:
                data+= client_socket.recv(24*1024)
            frameData = data[:msgSize]
            data = data[msgSize:]
            frame = pickle.loads(frameData)
            cv2.imshow("Received",frame)
            key = cv2.waitKey(1)
            if key == ord('q') : raise socket.error
        except socket.error:
            clients.pop(client_socket)
            break

while True:
    client_socket,addr = server_socket.accept()
    print("Connection from",addr)
    clients[client_socket] = threading.Thread(target=handle_client, args =(client_socket,))
    clients[client_socket].start()
