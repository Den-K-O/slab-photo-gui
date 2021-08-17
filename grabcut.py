import numpy as np
import time
import cv2
from matplotlib import pyplot as plt

def process_image(image_input):
    start = time.time()
    img = cv2.imread(image_input)
    print("image size:", img.shape[:2])
    scale_percent = 25 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)

    dim = (width, height)
      
    # resize image
    resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    mask = np.zeros(resized.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    #points=calibrate(resized)

    # show histogram
    # from matplotlib import pyplot as plt
    img_hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
    # color = ('h','s','v')
    # for i,col in enumerate(color):
        # histr = cv2.calcHist([img_hsv],[i],None,[256],[0,256])
        # plt.plot(histr)
        # plt.xlim([0,256])
    # plt.show()
    # cv2.waitKey(0)
    #cv2.imshow("obj shapeMask", img_hsv)
    lower = np.array([30, 0, 0])
    upper = np.array([255, 255, 255])
    shapeMask = cv2.inRange(img_hsv, lower, upper)
    #kernel = np.ones((7,7),np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(7,7))
    shapeMask=cv2.GaussianBlur(shapeMask,(9,9),cv2.BORDER_ISOLATED  )
    ret,shapeMask=cv2.threshold(shapeMask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    shapeMask=cv2.morphologyEx(shapeMask, cv2.MORPH_CLOSE, kernel,iterations = 3)
    shapeMask=cv2.bitwise_not(shapeMask)
    shapeMask=cv2.dilate(shapeMask,kernel,iterations = 3)
    x,y,w,h=cv2.boundingRect(shapeMask)
    print (x,y,w,h)
    img_2=resized.copy()
    cv2.rectangle(img_2,(x,y),(x+w,y+h),(0,255,0),2)
    img_2[shapeMask>127]+=np.array([50,-10,-10], dtype=np.uint8)
    cv2.imshow("obj shapeMask", img_2)
    points=[x,y],[x+w,y+h]
    print(points)
    rect = (points[0][0],points[0][1],points[1][0],points[1][1])
    mask_m=np.zeros(resized.shape[:2], np.uint8)
    mask_m[shapeMask > 0] = cv2.GC_PR_FGD
    mask_m[shapeMask == 0] = cv2.GC_BGD
    #cv2.grabCut(resized, mask, rect, bgdModel, fgdModel, 8, cv2.GC_INIT_WITH_RECT)
    (mask, bgModel, fgModel)=cv2.grabCut(resized, mask_m, None, bgdModel, fgdModel, 12, cv2.GC_INIT_WITH_MASK)
    print ("mask size: ",mask.shape[:2])
    #mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel,iterations = 2)
    mask = cv2.resize(mask, (img.shape[1],img.shape[0]), interpolation = cv2.INTER_NEAREST)
    mask3=np.zeros(mask.shape[:2], np.uint8)
    mask3[(mask==1) | (mask==3)] = 1
    mask3 = cv2.GaussianBlur(mask3,(11,11),cv2.BORDER_ISOLATED  )
    kernel = np.ones((3,3),np.uint8)
    #mask3 = cv2.erode(mask3,kernel,iterations = 1)

    valueMask = (mask3==1).astype("uint8") * 255
    cv2.namedWindow("mask", cv2.WINDOW_NORMAL)
    cv2.imshow("mask", valueMask)

    r_channel, g_channel, b_channel = cv2.split(img) 
    a_channel = np.where((mask3==1), 255, 0).astype('uint8')  

    img_RGBA = cv2.merge((r_channel, g_channel, b_channel, a_channel))
    cv2.imwrite("test.png", img_RGBA)

    contours, hierarchy = cv2.findContours(mask3, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(hierarchy)
    new_img=img.copy()
    #new_img[(mask3==1)] = 255
    cv2.drawContours(new_img, contours, -1, (0,255,0), 3)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        l,h=rect[1] if rect[1][0]>rect[1][1] else reversed(rect[1])
        area =  cv2.contourArea(cnt)
        print("slab area is: ",area/1000000,"m2")
        print("nonuniformity : ",area/(l*h)*100 ,"%")
        print("slab size is: ",l,"x",h, "mm")
        box = cv2.boxPoints(rect)    
        box = np.int0(box)
        print
        cv2.drawContours(new_img,[box],0,(0,0,255),3)
    cv2.namedWindow("main", cv2.WINDOW_NORMAL)
    cv2.imshow("main", new_img)
    end = time.time()
    print ("Calculation time: ",end-start)
    cv2.waitKey(0)

if __name__=='__main__':
    process_image('5.jpg')