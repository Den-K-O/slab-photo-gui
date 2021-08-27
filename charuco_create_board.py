import cv2
import matplotlib.pyplot as plt

aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
board = cv2.aruco.CharucoBoard_create(5, 8, 25, 20, aruco_dict)
print (help(board.draw))
plot=board.draw((3402 , 5102),100)
board.draw((3402 , 5102),plot,100)
cv2.namedWindow("main", cv2.WINDOW_NORMAL)
cv2.imshow("main", plot)
cv2.waitKey(0) 
cv2.imwrite('markerboard.tiff', plot)

# printing this
# aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_6X6_1000)
# board = cv2.aruco.CharucoBoard_create(5, 8, 25, 20, aruco_dict)
# print (help(board.draw))
# plot=board.draw((3402 , 5102),100)
# board.draw((3402 , 5102),plot,100)
# cv2.namedWindow("main", cv2.WINDOW_NORMAL)
# cv2.imshow("main", plot)
# cv2.waitKey(0) 
# cv2.imwrite('markerboard.tiff', plot)