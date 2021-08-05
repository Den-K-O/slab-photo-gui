import io
import os
import ftplib
import sys
import json
from PIL import Image
import tempfile

def load_to_ftp():
    session = ftplib.FTP('192.168.1.251','ftpbot','123456') # test_local
    session.cwd("/images")
    tfile = tempfile.NamedTemporaryFile()
    #fname = tmp.name
    tfile.write(b"Testing")
    tfile.flush()
    tfile.seek(0)  # This will rewind the curso
    session.storbinary('STOR '+"test"+'.txt', tfile)
    tfile.close()
    session.quit()

if __name__=="__main__":
    load_to_ftp()
