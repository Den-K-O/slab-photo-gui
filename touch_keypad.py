import PySimpleGUI as sg
import time

def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key))

def keypad():
    sg.theme('Topanga')
    p=((8,8),(2,2))
    my_font = ("Consolas", 24)
    column = [[sg.Button('0',pad=p,size=(5,1))]]
    layout = [
              [sg.Text(size=(20, 1), font=('Consolas', 25), text_color='white', key='input',pad=((50,50),(0,0)))],
              [sg.Button('1',pad=p), sg.Button('2',pad=p), sg.Button('3',pad=p),sg.Button('OK',pad=p)],
              [sg.Button('4',pad=p), sg.Button('5',pad=p), sg.Button('6',pad=p),sg.Button('C',pad=p)],
              [sg.Button('7',pad=p), sg.Button('8',pad=p), sg.Button('9',pad=p)],
              [sg.Text('', pad=((52,52),(0,0)),key='-EXPAND2-'),# the thing that expands from left
               sg.Column(column, vertical_alignment='top', justification='left',  k='-C-', size=(120,60)),sg.Text('', pad=((50,50),(0,0)),key='-EXPAND3-'),sg.Button('Назад',pad=p),]] 
              #[collapse([[sg.Button('dummy1',pad=p)]],"-1-"),sg.Button('0',pad=p),collapse([[sg.Button('dummy1',pad=p)]],"-2-"),sg.Button('Назад',pad=p)]]

    window = sg.Window('Keypad', layout, default_button_element_size=(4,1), font=my_font, auto_size_buttons=False, grab_anywhere=False, size=(480, 320), no_titlebar=True, location=(0, 0), keep_on_top=True,  finalize=True)
    #window['-C-'].expand(True, True, True)    
    #window['-EXPAND2-'].expand(True, False, True)
    
    # Loop forever reading the window's values, updating the Input field
    keys_entered = ''
    while True:
        event, values = window.read()  # read the window
        if event == sg.WIN_CLOSED:  # if the X button clicked, just exit
            break
        if event == 'C':  # clear keys if clear button
            keys_entered = ''
        elif event in '1234567890':
            
            keys_entered += str(event)
            # add the new digit
        elif event == 'OK':
            #keys_entered = values['input']
            window.close()
            return int(keys_entered)  # output the final string
            
        elif event == 'Назад':
            window.close()
            return
        
        window['input'].update(keys_entered)  # change the window to reflect current key string   
    
    
    
if __name__=="__main__":
    print(keypad())