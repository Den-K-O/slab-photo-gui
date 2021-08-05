import time
import picamera
from PIL import Image
import ftplib
import tempfile

def load_to_ftp():
    session = ftplib.FTP('192.168.1.251','ftpbot','123456') # test_local
    session.cwd("/images")
    tfile = tempfile.NamedTemporaryFile()
    #fname = tmp.name
    
    with picamera.PiCamera() as camera:
        camera.start_preview()
        time.sleep(2)
        camera.capture(tfile, format='jpeg')
    
    #tfile.write(b"Testing")
    #tfile.flush()
    tfile.seek(0)  # This will rewind the cursor
    session.storbinary('STOR '+"test"+'.jpg', tfile)
    tfile.close()
    session.quit()

if __name__=="__main__":
    load_to_ftp()
