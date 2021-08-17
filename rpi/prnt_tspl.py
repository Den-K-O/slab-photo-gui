#!/usr/bin/env python3
PRINTER = '/dev/usb/lp0' # the printer device
DOTS_MM = 8 # printer dots per mm, 8 == 203 dpi
WIDTH_MM = 56 # sticker width, mm
HEIGHT_MM =40  # sticker height, mm
GAP_MM = 1.8 # sticker gap, mm
FONT = "5" # built-in vector font, scalable by X and Y
FONT_X_MULT = 4 # font multiplication, for "0" font is size in points
FONT_Y_MULT = 4 # font multiplication, for "0" font is size in points
import os
import sys
import time
import re
from PIL import Image
class Printer:
    width = WIDTH_MM * DOTS_MM
    height = HEIGHT_MM * DOTS_MM
    def __init__(self):
        self.printer =os.open(PRINTER, os.O_RDWR)
        self.commands = []
     def printer_status(self):
        os.write(self.printer, b"\x1B!?\r\n")
        status = os.read(self.printer, 8)
        print(status[1:5].decode('ascii'))
        return status[1:5].decode('ascii')

    def can_print(self):
        return re.fullmatch(r'[@BCFPW]@@@', self.printer_status()) is not None

    def wait_printer(self):
        if not self.can_print():
            print('...waiting printer...', end='',file=sys.stderr)
            time.sleep(0.5)
            while not self.can_print():
                print('.', end='', file=sys.stderr)
                time.sleep(1)
            print(file=sys.stderr)
    def page_setup(self):
        self.command('SIZE {} mm,{}mm'.format(WIDTH_MM, HEIGHT_MM))
        self.command('GAP {} mm,0mm'.format(GAP_MM))
        self.command('DIRECTION 1')

    def print(self):
        #self.wait_printer()
        self.page_setup()
        for cmd in self.commands:
            self.command(cmd)
        self.command('PRINT 1,1')

    def command(self, cmd):

        if isinstance(cmd,bytes):
            #print(cmd)
            os.write(self.printer, cmd)
        else:
            print(cmd)
            os.write(self.printer, cmd.encode("utf-8"))
        try:
            if 'BITMAP' not  in cmd:
                os.write(self.printer, b'\r\n')
        except:
            os.write(self.printer, b'\r\n')

def img_to_bytes(img):
    im = Image.open(img)
    im=im.resize((416,360))
    thresh = 200
    fn = lambda x : 255 if x < thresh else 0
    r = im.convert('L').point(fn, mode='1')
    bytes = r.tobytes()
    w = im.width
    h = im.height
    return bytes, w, h

if __name__ == '__main__':
    print("starting")
    image = 'fragile.bmp'
    my_bytes,w,h =img_to_bytes(image)
    print ("image loaded:", w,"x",h)
    x=0
    y=0
    w_bytes = w//8
    h_rows = h
    p = Printer()
    print ("printer initiated")
    p.commands.append('CLS')
    #p.commands.append(f'BITMAP {x},{y}, {w_bytes}, {h_rows}, 0,')
    #p.commands.append(my_bytes)
    p.commands.append('TEXT 24,112,"5",0,2,2,"S12345" ')
    print ("commands ready:")
    #print(p.commands)
    p.print()
    print("finished")
    print(p.printer_status())

