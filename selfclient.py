import socket
import cv2
import pickle
import struct
# Client socket
# create an INET, STREAMing socket : 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
# host_ip = '<localhost>'# Standard loopback interface address (localhost)
port = 10050 # Port to listen on (non-privileged ports are > 1023)
# now connect to the web server on the specified port number
client_socket.connect((host_ip,port)) 
camera = cv2.VideoCapture(0)
scaleFac = 0.8

while True:
    ret, frm = camera.read()
    frm = cv2.resize(frm,(int(frm.shape[1]*scaleFac),int(frm.shape[0]*scaleFac)))
    a = pickle.dumps(frm)
    message = struct.pack("Q",len(a))+a
    try:
        client_socket.sendall(message)
        print(f"Frame size = {len(message)}\t",end='\r')
        cv2.imshow("ClientVideo",frm)
        cv2.waitKey(50)
    except:
        print("Connection lost")
        break
