import PySimpleGUI as sg



layout = [[sg.Text('Enter Your Passcode')],
          [sg.Text(size=(15, 1), font=('Consolas', 18), text_color='white', key='input')],
          [sg.Button('1'), sg.Button('2'), sg.Button('3')],
          [sg.Button('4'), sg.Button('5'), sg.Button('6')],
          [sg.Button('7'), sg.Button('8'), sg.Button('9')],
          [sg.Button('Submit'), sg.Button('0'), sg.Button('Clear')],
          [sg.Text(size=(15, 1), font=('Helvetica', 18), text_color='white', key='out')]]

window = sg.Window('Keypad', layout, default_button_element_size=(5,2), auto_size_buttons=False)

# Loop forever reading the window's values, updating the Input field
keys_entered = ''
while True:
    event, values = window.read()  # read the window
    if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
        break
    if event == 'Clear':  # clear keys if clear button
        keys_entered = ''
    elif event in '1234567890':
        
        keys_entered += str(event)
        # add the new digit
    elif event == 'Submit':
        #keys_entered = values['input']
        window['out'].update(keys_entered)  # output the final string

    window['input'].update(keys_entered)  # change the window to reflect current key string   