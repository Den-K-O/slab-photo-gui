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

#DEBUG = False
DEBUG = True
class Printer:
    
    def __init__(self):
        self.PRINTER = '/dev/usb/lp0' # the printer device 
        self.DOTS_MM = 8 # printer dots per mm, 8 == 203 dpi 
        self.WIDTH_MM = 56 # sticker width, mm 
        self.HEIGHT_MM =40  # sticker height, mm 
        self.GAP_MM = 1.8 # sticker gap, mm 
        self.FONT = "5" # built-in vector font, scalable by X and Y 
        self.FONT_X_MULT = 2 # font multiplication, for "0" font is size in points 
        self.FONT_Y_MULT = 2 # font multiplication, for "0" font is size in points 
        self.x0=0 # offset
        self.y0=0 # offset
        self.width = self.WIDTH_MM * self.DOTS_MM
        self.height = self.HEIGHT_MM * self.DOTS_MM
        self.printer =os.open(self.PRINTER, os.O_RDWR) 
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
        self.command('SIZE {} mm,{}mm'.format(self.WIDTH_MM, self.HEIGHT_MM))
        self.command('GAP {} mm,0mm'.format(self.GAP_MM)) 
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
            
    def print_image(self,image):
    my_bytes,w,h =self.img_to_bytes(image)
    x=0
    y=0
    w_bytes = w//8
    h_rows = h
    header = f'BITMAP {x},{y}, {w_bytes}, {h_rows}, 0,'
    payload = my_bytes
    self.commands.append(header)
    self.commands.append(payload)
    
    def clear_print_buffer(self):
        self.commands.append('CLS')
     
    def img_to_bytes(self,img):
        im = Image.open(img)
        im=im.resize((416,360))
        thresh = 200
        fn = lambda x : 255 if x < thresh else 0 
        r = im.convert('L').point(fn, mode='1') 
        bytes = r.tobytes()
        w = im.width 
        h = im.height
        return bytes, w, h
    
    def print_text(self,text,x=self.x0,y=self.y0,font='5',rotation=0,x_mult=1,y_mult=1):
        self.commands.append(f'TEXT {x},{y},"{font}",{rotation},{x_mult},{y_mult},"{text}"')




if __name__ == '__main__':
    if DEBUG: print("starting")    
    p = Printer() 
    if DEBUG: print ("printer initiated")
    p.clear_print_buffer()
    p.print_text("S12345",x=24,y=112,x_mult=2,y_mult=2)   
    if DEBUG: print ("commands ready:")
    if DEBUG: print(p.commands)
    p.print()
    if DEBUG: print("finished")
    if DEBUG: print(p.printer_status())

