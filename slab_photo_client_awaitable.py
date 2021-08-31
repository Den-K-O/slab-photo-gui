import socket
from time import time, sleep
from io import BytesIO
import asyncio
import functools
import PySimpleGUI as sg      
import datetime
import undistort_charuco
import write_to_DB
from prnt_tspl import Printer,print_id

DEBUG=False
#DEBUG=True

def open_socket():
    HOST = '192.168.1.75'
    PORT = 10000    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if DEBUG: print ('client socket opened')
    server_address = (HOST, PORT)  
    sock.connect(server_address)
    if DEBUG: print ('connected to server')
    
    return sock

async def request_photo(sock):
    loop = asyncio.get_running_loop()
    global progress    
    chunk_size=4096
    mystream = BytesIO()
    recieved=0
    while True:    
        #try:
        
        data = await loop.run_in_executor(None, functools.partial(sock.recv,chunk_size))
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
                progress = recieved*100 // size
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
    if DEBUG: print ('closing socket')
    sock.close()

async def get_photo(sock,row,p,mapx,mapy):    
    
    start = time()
    photo = await request_photo(sock)     
            
    # get name from slabs.id
    id=write_to_DB.create_entry(row)
    print("Slab added to DB, id: ",id, "printer: ",p)
    
    name = str(id)
    try:
        print_id(id,p)
    except:
        print ("Test - no printer connected; id: ",id)
    undistort_charuco.undistort_image(photo,name,mapx,mapy)        
    end = time()
    if DEBUG: print("sending time: ", end-start)
    # create_photo_entry_in_DB
    # save_photo_with_DB_id  
    # photo processing will be done in another background process
    return id
    
async def progbar_check():
    # global dots
    global progress
    progress = 0
    dots = 3    
    window = create_progressbar()
    
    while True:
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=100)
        if event == 'Cancel' or event == sg.WIN_CLOSED:
            break
            # update bar with loop value +1 so that bar eventually reaches the maximum
        if DEBUG: print (progress)
        window['-PROG-'].update(progress)
        if progress <100:
            if dots <=3:
                dots += 1            
            if dots >3:
                dots =0
            window['-TEXT-'].update('Завантажується зображення'+'.'*dots)
        else:
            window['-TEXT-'].update('Зображення завантажено')
            await asyncio.sleep(1.5)
            window.close()
            break
        await asyncio.sleep(0.2)

def create_progressbar():    
    sg.theme('Topanga')
    BAR_MAX = 100
    my_font = ("Consolas", 20)
    # layout the Window
    column = [[sg.Text('Завантажується зображення...',k='-TEXT-', font=my_font,size=(42,2),pad=((5,5),(7,7)))],
              [sg.ProgressBar(BAR_MAX, orientation='h', size=(42,30), key='-PROG-')],
             ]
    layout = [[sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],  # the thing that expands from top
              [sg.Text('', pad=(0,0),key='-EXPAND2-'),              # the thing that expands from left
               sg.Column(column, vertical_alignment='center', justification='center',  k='-C-')]]
    # create the Window
    window = sg.Window('Завантаження', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True, modal=True, finalize=True)
    window['-C-'].expand(True, True, True)
    window['-EXPAND-'].expand(True, True, True)
    window['-EXPAND2-'].expand(True, False, True)
    # loop that would normally do something useful    
    # done with loop... need to destroy the window as it's still open
    return window

async def main(slab_data,p,mapx,mapy):
    sock = open_socket()  
    row=slab_data   
    tasks = []
    t1=asyncio.create_task(progbar_check())
    t2=asyncio.create_task(get_photo(sock,row,p,mapx,mapy))    
    
    await t1
    id = await t2
       
    close_socket(sock) #in the end        
    return id 
    
if __name__=='__main__':
    row={
    "wood" : "горіх",
    "thickness": 60,
    }
    asyncio.run(main(row)) 
    