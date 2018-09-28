import numpy as np
import cv2

#Loading Calibration Data
calibrationData = np.load('camcalib_3.npz')
mtx = calibrationData['mtx']
dist = calibrationData['dist']
newcameramtx = calibrationData['newcameramtx']
roi = calibrationData['roi']
#Close File
calibrationData.close()
print mtx
print dist
print newcameramtx
print roi
x,y,w,h = roi

print x
print y
print w
print h

img = cv2.imread('c.jpg')
img = cv2.undistort(img, mtx, dist, None, newcameramtx)
#img = img[y:y+h, x:x+w]
#img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

#cv2.imshow('img', img)

cv2.imwrite("undistort_c0.png",img)




