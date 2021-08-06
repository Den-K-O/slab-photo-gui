import PySimpleGUI as sg

# sg.theme('Dark Green 7')
sg.theme('Topanga')      # Add some color to the window
my_font = ("Consolas", 22)
text_size=12
inputsize=12
button_size = 14

col1=[ 
           [sg.Txt('Дата початок',size=(text_size,1),font=my_font),sg.Input(key='-IN4-', size=(inputsize,1),font=my_font)],
           [sg.Txt('Дата кінець',size=(text_size,1),font=my_font),sg.Input(key='-IN5-', size=(inputsize,1),font=my_font)],           
         ]
col2=[ 
           [sg.CalendarButton('Оберіть дату',  target='-IN4-', format = "%d-%m-%Y",font=my_font,size=(button_size,1) )],
           [sg.CalendarButton('Оберіть дату',  target='-IN5-', format = "%d-%m-%Y",font=my_font,size=(button_size,1) )],
           [sg.Button('Записи', bind_return_key=True,font=my_font,size=(button_size,1))],
           [sg.Button('Exit',font=my_font,size=(button_size,1))]
         ]

layout = [ 
           [sg.Column(col1),sg.Column(col2)],           
         ]

window = sg.Window('Записи часу', layout, grab_anywhere=False, size=(720, 480), no_titlebar=True, location=(0, 0), keep_on_top=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
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
    
    else:
        break
