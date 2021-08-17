import asyncio
# import socket
from time import time, sleep
from io import BytesIO
from PIL import Image

DEBUG=False
DEBUG=True

async def get_image():    
    HOST = '192.168.1.75'
    PORT = 10000    
    reader, writer = await asyncio.open_connection(HOST, PORT)
    
    if DEBUG: print ('connected to server')
    
    for i in range(1):
        if DEBUG: print(f'iteration {i}')
        start = time()
        chunk_size=4096
    photo = BytesIO()
    recieved=0
    while True:    
        #try:
        data = await reader.read(chunk_size)
        
        try:
            txt = data.decode()
        except:
            txt = "DATA TRANSMISSION" 
        if data:
            if DEBUG: print ('answer = %s' % txt[:20])
            if txt.startswith('READY'):
                writer.write(b'GET IMAGE')
                await writer.drain()
                if DEBUG: print ('image request sent')
            
            elif txt.startswith('SIZE'):
                tmp = txt.split()
                size = int(tmp[1])
                if DEBUG: print ('got size')
                writer.write(b"GOT SIZE")
                await writer.drain()
                #chunk_size = 7168000

            elif txt.startswith('BYE'):
                pass
                break
                #sock.shutdown()

            elif data:                
                
                recieved+=len(data)
                if DEBUG: print(f'recieved: {recieved} of {size}')                                    
                photo.write(data)
                if recieved>=size:           
                    writer.write(b"GOT IMAGE") 
                    await writer.drain()
                    if DEBUG: print ('got image')
                    #chunk_size = 4096
                    if DEBUG: print ('--------------------------------------------------------------')
                    #close_socket(sock)
                    break
            #except:
            #    print('exiting process')
            #    break          
        with open('image_from_camera.jpeg',"wb") as outfile:
            outfile.write(photo.getbuffer())
        end = time()
        if DEBUG: print("sending time: ", end-start)
        # create_photo_entry_in_DB
        # save_photo_with_DB_id  
        # photo processing will be done in another background process
        sleep(0.2)
    print ('closing socket')
    writer.close()
    await writer.wait_closed()

if __name__=='__main__': 
    asyncio.run(get_image())



