import cv2
import numpy as np

def mke_coordinate(image,line_param):
    slope, intecept = line_param
    y1 = int(image.shape[0])
    y2 = int(y1 *(3/5))
    x1 = int((y1-intecept)/slope)
    x2 = int((y2-intecept)/slope)
    return np.array([x1, y1, x2, y2])

def avarage_line_intercept(image,lines):
    left_fit =[]
    right_fit =[]

    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, y1),(x2, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        if slope <0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_line_avg = np.average(left_fit,axis=0)
    right_line_avg = np.average(right_fit,axis=0)

    left_line = mke_coordinate(image, left_line_avg)
    right_line = mke_coordinate(image, right_line_avg)

    return np.array([left_line, right_line])
        
def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    cany = cv2.Canny(blur,50,150)
    return cany
def display_line(image,lines):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            cv2.line(line_image, (x1,y1), (x2,y2), (255,0,0), 10)
    return line_image

def region_of_interest(image):
    height = image.shape[0]
    tringale = np.array([
        [(200, height),(1100, height),(550, 250)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, tringale, 210)
    masked_image = cv2.bitwise_and(image,mask)
    return masked_image

image = cv2.imread("test_image.jpg")
lane_image = np.copy(image)
cany_image = canny(lane_image)
croped_image = region_of_interest(cany_image)
line = cv2.HoughLinesP(croped_image, 2, np.pi/180, 100, np.array([]), minLineLength=40, maxLineGap =5)
avarage_line = avarage_line_intercept(lane_image,line)
line_image = display_line(lane_image,avarage_line)
combo_image = cv2.addWeighted(lane_image, 0.8, line_image, 1, 1)
cv2.imshow("results",combo_image)
cv2.waitKey(0)