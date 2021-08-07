import PySimpleGUI as sg
import base64

# sg.theme('Dark Green 7')
sg.theme('Topanga')      # Add some color to the window
my_font = ("Consolas", 22)
counter_font = ("Consolas", 25)
text_size=14
inputsize=14
button_size = 18

col1=[            
           [sg.Button('Горіх',key='-WOOD-',font=my_font,size=(button_size,2),pad=((5,5),(12,12)))],
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
        if int(values['-THCK-'])<150: window['-THCK-'].update(str(int(values['-THCK-'])+5))
        
    
    if event == '-DN-':
        if int(values['-THCK-'])>0: window['-THCK-'].update(str(int(values['-THCK-'])-5))

    #else:
    #    break
