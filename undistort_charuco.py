from charuco import calibrate_charuco
from utils import load_coefficients, save_coefficients
import cv2

# Load coefficients
filename="image_26-08-2021_13_23_24"
mtx, dist = load_coefficients('calibration_charuco.yml')
original = cv2.imread(f'calibration_test\\{filename}.jpeg')
dst = cv2.undistort(original, mtx, dist, None, mtx)
cv2.imwrite('out\\undisted.jpg', dst)
cv2.imwrite('out\\original.jpg', original)