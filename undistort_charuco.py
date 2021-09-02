from utils import load_coefficients, save_coefficients
import cv2
import sys
import numpy as np
import platform
from time import time

TEST = platform.system()=='Windows'

if TEST:
    location = 'photos\\'
    
else:
    location = '/home/pi/shared/'

# Load coefficients
#mtx, dist = load_coefficients('calibration_charuco.yml')

try:
    filename=sys.argv[1]
except:
    pass 
    
def create_opencv_image_from_stringio(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)

def undistort_file(filename,mapx, mapy):
    #mtx, dist = load_coefficients('calibration_charuco.yml')
    original = cv2.imread(f'calibration_test\\{filename}.jpeg')
    #dst = cv2.undistort(original, mtx, dist, None, mtx)
    dst=cv2.remap(original, mapx, mapy, cv2.INTER_LINEAR)
    cv2.imwrite(f'out\\{filename}.jpg', dst)
    cv2.imwrite(f'out\\{filename}_undist.jpg', original)

def undistort_image(img,filename,mapx, mapy):
    #mtx, dist = load_coefficients('calibration_charuco.yml')
    start = time()
    original = create_opencv_image_from_stringio(img,cv2.IMREAD_ANYCOLOR+cv2.IMREAD_ANYDEPTH)
    end = time()
    bytes_to_opencv = end-start
    #dst = cv2.undistort(original, mtx, dist, None, mtx)
    start = time()
    dst=cv2.remap(original, mapx, mapy, cv2.INTER_LINEAR)
    cv2.imwrite(f'{location}{filename}.jpg', dst)
    end = time()
    undistort_time = end-start
    print ("undistort time: ", bytes_to_opencv,"+",undistort_time)
    cv2.imwrite(f'{location}{filename}_raw.jpg',original)