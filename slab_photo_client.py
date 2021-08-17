import socket
from time import time, sleep
from io import BytesIO
from PIL import Image

DEBUG=False
DEBUG=True

def open_socket():
    HOST = '192.168.1.75'
    PORT = 10000    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if DEBUG: print ('client socket opened')
    server_address = (HOST, PORT)  
    sock.connect(server_address)
    if DEBUG: print ('connected to server')
    
    return sock

def request_photo(sock):    
    chunk_size=4096
    mystream = BytesIO()
    recieved=0
    while True:    
        #try:
        data = sock.recv(chunk_size)
        try:
            txt = data.decode()
        except:
            txt = "DATA TRANSMISSION" 
        if data:
            if DEBUG: print ('answer = %s' % txt[:20])
            if txt.startswith('READY'):
                sock.sendall(b'GET IMAGE')
                if DEBUG: print ('image request sent')
            
            elif txt.startswith('SIZE'):
                tmp = txt.split()
                size = int(tmp[1])
                if DEBUG: print ('got size')
                sock.sendall(b"GOT SIZE")
                #chunk_size = 7168000

            elif txt.startswith('BYE'):
                pass
                break
                #sock.shutdown()

            elif data:                
                
                recieved+=len(data)
                if DEBUG: print(f'recieved: {recieved} of {size}')                                    
                mystream.write(data)
                if recieved>=size:           
                    sock.send(b"GOT IMAGE") 
                    if DEBUG: print ('got image')
                    #chunk_size = 4096
                    if DEBUG: print ('--------------------------------------------------------------')
                    #close_socket(sock)
                    break
            #except:
            #    print('exiting process')
            #    break
    return mystream


def close_socket(sock):
    print ('closing socket')
    sock.close()

if __name__=='__main__':
    
    sock = open_socket()
    for i in range(1):
        if DEBUG: print(f'iteration {i}')
        start = time()
        photo = request_photo(sock)
        with open('image_from_camera.jpeg',"wb") as outfile:
            outfile.write(photo.getbuffer())
        end = time()
        if DEBUG: print("sending time: ", end-start)
        # create_photo_entry_in_DB
        # save_photo_with_DB_id  
        # photo processing will be done in another background process
        sleep(0.2)
    close_socket(sock)
    
    
    