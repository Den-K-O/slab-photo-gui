import PySimpleGUI as sg
import base64
import math
import slab_photo_client_awaitable
import asyncio
from prnt_tspl import Printer,print_id
import numpy as np
import touch_keypad
import platform
import write_to_DB

TEST = platform.system()=='Windows'

if TEST:   
    working_dir=''
else:
    working_dir= '/home/pi/py_scripts/slab-photo-gui/'


mapx=np.load(working_dir+'mapx.npy')
mapy=np.load(working_dir+'mapy.npy')

try:
    p=Printer()
except:
    p=1
print("printer=", p )   
sg.theme('Topanga')      # Add some color to the window
my_font = ("Consolas", 22)
counter_font = ("Consolas", 25)
text_size=14
inputsize=14
button_size = 18

#DEBUG = False
DEBUG = True

# def print_id(id,p):
    # if DEBUG: print("starting")  
    # if DEBUG: print ("printer initiated")
    # p.clear_print_buffer()
    # p.print_text("S"+str(id).zfill(5),x=24,y=112,x_mult=2,y_mult=2)   
    # if DEBUG: print ("commands ready:")
    # if DEBUG: print(p.commands)
    # p.print(3)
    # if DEBUG: print("finished")
    
wood_species = ["Горіх",
                "Дуб",
                "Ясен",
                "В`яз",
                "В`яз столяр.",
                "Тополя",
                "Клен",
                "Морений дуб",    
                "Амер. горіх",
                "Маслина",
                "Акація",                
                None]

def start_window():
    col1=[            
               [sg.Button(wood_species[0],key='-WOOD-',font=my_font,size=(button_size,1),pad=((5,5),(5,5)))],
               [sg.Button('Слеб',key='-PHOTO-',font=my_font,size=(button_size,1),pad=((5,5),(3,5)))],
               [sg.Button('Підбір',key='-PHOTO_GROUP-',font=my_font,size=(button_size,1),pad=((5,5),(3,5)))],
               [sg.Button('Списати', key='-WRITE_OFF-', font=my_font, size=(button_size, 1), pad=((5, 5), (3, 5)))]
               
         ]
    col2=[ 
               [sg.Button('',key='-UP-', image_filename=working_dir+"up.png",image_size=(80,80),image_subsample=2, font=my_font,size=(button_size,2), pad=((5,5),(5,5)))],
               [sg.Input(key='-THCK-', default_text = "30", size=(4,15),font=counter_font,pad=((5,5),(5,5)), justification='center')],
               [sg.Button('',key='-DN-', image_filename=working_dir+"dn.png",image_size=(80,80),image_subsample=2, font=my_font,size=(button_size,2), pad=((5,5),(5,5)))],
               
             ]

    layout = [ 
               [sg.Column(col1,size=(320,240),element_justification = 'center'),sg.Column(col2,size=(160,240),element_justification = 'center')],
               #[sg.Button('X',font=("Consolas", 15),size=(2,1),pad=((5,5),(12,12))),
               [sg.StatusBar( text='...status...', key='-status_bar-',font=my_font , justification='center',size=(40,1))]
             ]

    window = sg.Window('Параметри слеба', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True,  finalize=True)
    return window

st_window=start_window()

wood_species_lst = wood_species.copy()

def wood_selection_window(wood_species):  
    def button_or_nothing(name):        
        if name:
            return sg.Button(name,font=my_font,size=(5,2),pad=((2,2),(2,2)))
        else:
            return sg.Text("")
    MAX_COL = 3
    MAX_ROWS = 4
    #print (MAX_ROWS)
    layout =  [[button_or_nothing(wood_species_lst.pop()) for j in range(MAX_COL)] for i in range(MAX_ROWS)]

    window = sg.Window('Вибір породи дерева', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True, modal=True, finalize=True)
    
    return window

# def make_photo_window(wood_species):  
    # layout =  [[]
              # ]

    # window = sg.Window('Очікується фото', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True, modal=True, finalize=True)
    
    # return window

while True:
    event, values = st_window.read()

    if event == sg.WIN_CLOSED or event == 'X':
        break  
    
    if event == '-PHOTO-':
        row={
        "wood" : st_window['-WOOD-'].ButtonText.lower(),
        "thickness": int(values['-THCK-']),
        }
        #print(row)
        id = asyncio.run(slab_photo_client_awaitable.main(row,p,mapx,mapy))
        #print("id returned to GUI: ",id)
        st_window['-status_bar-'].update("OK, slab id: "+str(id))
    
    if event == '-PHOTO_GROUP-':        
        row=touch_keypad.keypad()
        if isinstance(row,int):
            #print(row)
            id = asyncio.run(slab_photo_client_awaitable.main(row,p,mapx,mapy))
            #print("id returned to GUI: ",id)
            st_window['-status_bar-'].update("OK, order No:"+str(id))
        else:
            pass
        
        
    
    if event == '-WOOD-':     ### select wood species ###
        wood_species_lst = list(reversed(wood_species.copy()))
        wood_window=wood_selection_window(wood_species)  
        while True:
            event, values = wood_window.read()
            #print(event)
            if event in wood_species:
                st_window['-WOOD-'].update(event)
                wood_window.close()
                break

    if event == '-WRITE_OFF-':
        slab_id=touch_keypad.keypad()
        if slab_id:
            print(slab_id)
            write_to_DB.use_slab(slab_id)
            st_window['-status_bar-'].update("write off, slab id: "+str(slab_id))
    
   
    if event == '-UP-':       ### change slab thickness ###   
        if int(values['-THCK-'])<150: st_window['-THCK-'].update(str(int(values['-THCK-'])+5))
        
    
    if event == '-DN-':       ### change slab thickness ###
        if int(values['-THCK-'])>0: st_window['-THCK-'].update(str(int(values['-THCK-'])-5))
    
    #else:
    #    break
