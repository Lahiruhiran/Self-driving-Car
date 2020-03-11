import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    cany = cv2.Canny(blur,50,150)
    return cany

def region_of_interest(image):
    height = image.shape[0]
    tringale = np.array([
        [(200, height),(1100, height),(550, 250)]
        ])
    mask = np.zeros_like(image)
    cv2.fillPoly(mask, tringale, 210)
    return mask

image = cv2.imread("test_image.jpg")
lane_image = np.copy(image)
cany = canny(lane_image)
cv2.imshow("results",region_of_interest(cany))
cv2.waitKey(0)