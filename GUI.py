import PySimpleGUI as sg
import base64

# sg.theme('Dark Green 7')
sg.theme('Topanga')      # Add some color to the window
my_font = ("Consolas", 22)
counter_font = ("Consolas", 25)
text_size=14
inputsize=14
button_size = 18

wood_species = ["Горіх",
                "Дуб",
                "Ясен",
                "В'яз",
                "Тополя",
                "Клен",
                "Морений дуб",    
                "Амер. горіх",
                "Маслина"]

def start_window():
    col1=[            
               [sg.Button(wood_species[0],key='-WOOD-',font=my_font,size=(button_size,2),pad=((5,5),(12,12)))],
               [sg.Button('Фото',key='-PHOTO-',font=my_font,size=(button_size,2),pad=((5,5),(12,12)))]          
               
         ]
    col2=[ 
               [sg.Button('',key='-UP-', image_filename="up.png",image_size=(80,80),image_subsample=2, font=my_font,size=(button_size,2), pad=((5,5),(5,5)))],
               [sg.Input(key='-THCK-', default_text = "30", size=(4,15),font=counter_font,pad=((5,5),(5,5)), justification='center')],
               [sg.Button('',key='-DN-', image_filename="dn.png",image_size=(80,80),image_subsample=2, font=my_font,size=(button_size,2), pad=((5,5),(5,5)))],
               
             ]

    layout = [ 
               [sg.Column(col1,size=(320,240),element_justification = 'center'),sg.Column(col2,size=(160,240),element_justification = 'center')],
               [sg.Button('X',font=("Consolas", 15),size=(2,1),pad=((5,5),(12,12))),sg.StatusBar( text='...status...', key='status_bar',font=my_font , justification='center')]
             ]

    window = sg.Window('Параметри слеба', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True,  finalize=True)
    return window

st_window=start_window()

wood_species_lst = wood_species.copy()

def wood_selection_window(wood_species):  
    MAX_COL = 3
    MAX_ROWS = len(wood_species)//MAX_COL
    #print (MAX_ROWS)
    layout =  [[sg.Button(wood_species_lst.pop(),font=my_font,size=(7,2),pad=((2,2),(2,2))) for j in range(MAX_COL)] for i in range(MAX_ROWS)]

    window = sg.Window('Вибір породи дерева', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True, modal=True, finalize=True)
    
    return window

def make_photo_window(wood_species):  
    layout =  [[]
              ]

    window = sg.Window('Очікується фото', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True, modal=True, finalize=True)
    
    return window

while True:
    event, values = st_window.read()

    if event == sg.WIN_CLOSED or event == 'X':
        break  
    
    
    
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
    
   
    if event == '-UP-':       ### change slab thickness ###   
        if int(values['-THCK-'])<150: st_window['-THCK-'].update(str(int(values['-THCK-'])+5))
        
    
    if event == '-DN-':       ### change slab thickness ###
        if int(values['-THCK-'])>0: st_window['-THCK-'].update(str(int(values['-THCK-'])-5))
    
    #else:
    #    break
