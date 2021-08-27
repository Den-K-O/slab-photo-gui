from utils import load_coefficients, save_coefficients
import cv2
import sys
import numpy as np

# Load coefficients
mtx, dist = load_coefficients('calibration_charuco.yml')

try:
    filename=sys.argv[1]
except:
    pass 
    
def create_opencv_image_from_stringio(img_stream, cv2_img_flag=0):
    img_stream.seek(0)
    img_array = np.asarray(bytearray(img_stream.read()), dtype=np.uint8)
    return cv2.imdecode(img_array, cv2_img_flag)

def undistort_file(filename):
    #mtx, dist = load_coefficients('calibration_charuco.yml')
    original = cv2.imread(f'calibration_test\\{filename}.jpeg')
    dst = cv2.undistort(original, mtx, dist, None, mtx)
    cv2.imwrite(f'out\\{filename}.jpg', dst)
    cv2.imwrite(f'out\\{filename}_undist.jpg', original)

def undistort_image(img,filename):
    #mtx, dist = load_coefficients('calibration_charuco.yml')
    original = create_opencv_image_from_stringio(img,cv2.IMREAD_ANYCOLOR+cv2.IMREAD_ANYDEPTH)
    dst = cv2.undistort(original, mtx, dist, None, mtx)
    cv2.imwrite(f'photos\\{filename}.jpg', dst)
    #cv2.imwrite(f'photos\\out\\test_undist.jpg', original)