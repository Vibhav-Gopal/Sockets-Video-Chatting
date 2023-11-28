import socket
import cv2
import pickle
import struct
import threading

def renderHandler(frames):
    #TODO
    ...



def listenServer(clientSocket):
    data = b""
    while True:
        try: 
            frames=[]
            payload_size = struct.calcsize("Q")
            while len(data)<payload_size:
                packet = clientSocket.recv(1)
                if not packet : break
                data+=packet
            numFrames = data[:payload_size]
            data = data[payload_size:]
            for i in range(numFrames):
                while len(data)<payload_size:
                    packet = clientSocket.recv(1)
                    if not packet : break
                    data+=packet
                packedSize = data[:payload_size]
                data = data[payload_size:]
                frameSize = struct.unpack("Q",packedSize)[0]
                while len(data)<frameSize:
                    data+=clientSocket.recv(24*1024)
                frame = data[:frameSize]
                data = data[frameSize:]
                frames.append(frame)

            renderHandler(frames)
            #TODO Render Frames here
            
            key = cv2.waitKey(1)
            if key == ord('q') : raise socket.error
        except socket.error:
            exit(0)
    

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_name  = socket.gethostname()
host_ip = socket.gethostbyname(host_name)

port = 10050 # Port to listen on (non-privileged ports are > 1023)

client_socket.connect((host_ip,port)) 
print("Client to server connection established")
receiveThread = threading.Thread(target=listenServer,args=(client_socket,))
receiveThread.start()
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
        # cv2.imshow("ClientVideo",frm)
        cv2.waitKey(50)
    except:
        print("Connection lost")
        break
