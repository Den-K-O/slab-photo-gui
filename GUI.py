import PySimpleGUI as sg
import base64

# sg.theme('Dark Green 7')
sg.theme('Topanga')      # Add some color to the window
my_font = ("Consolas", 20)
counter_font = ("Consolas", 25)
text_size=14
inputsize=14
button_size = 14

col1=[ 
           [sg.Button('X',font=my_font,size=(5,2),pad=((10,10),(10,10)))],
           [sg.Button('Горіх',key='-WOOD-',font=my_font,size=(button_size,2),pad=((10,10),(10,10)))],
           [sg.Button('Фото',key='-PHOTO-',font=my_font,size=(button_size,2),pad=((10,10),(10,10)))]          
           
     ]
col2=[ 
           [sg.Button('',key='-UP-', image_filename="up.png",image_size=(80,80),image_subsample=2, font=my_font,size=(button_size,2), pad=((10,10),(10,10)))],
           [sg.Input(key='-THCK-', default_text = "30", size=(4,15),font=counter_font,pad=((10,10),(10,10)), justification='center')],
           [sg.Button('',key='-DN-', image_filename="dn.png",image_size=(80,80),image_subsample=2, font=my_font,size=(button_size,2), pad=((10,10),(10,10)))],
           
         ]

layout = [ 
           [sg.Column(col1),sg.Column(col2)],
           [sg.StatusBar( text='status', key='status_bar', font=my_font )]
         ]

window = sg.Window('Записи часу', layout, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True,  finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'X':
        break  
    
    if event == 'Записи':
        try:            
            if values['-IN5-']:
                pass
            else:
                pass
                             
            sg.popup_scrolled(entries, size=(80, None), title="Записи часу за "+str(values['-IN4-']), font=("Consolas", 11))               
            
        except IndexError:
            print (" No statements " )          
            sg.popup(" No statements ")
            # sg.popup_scrolled(output, size=(80, None), title="Виписка")
        except Exception as e:
            print(e)
            sg.popup('Увага!','Перевірте правильність введених даних!')
        # window['-OUTPUT-'].update(calc)
    
    if event == '-UP-':        
        window['-THCK-'].update(str(int(values['-THCK-'])+1))
        
    
    if event == '-DN-':
        window['-THCK-'].update(str(int(values['-THCK-'])-1))

    #else:
    #    break
