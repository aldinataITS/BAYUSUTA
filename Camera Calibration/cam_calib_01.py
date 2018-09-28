import numpy as np
import cv2
import glob

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
print ("step 1")

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*9,3), np.float32)
objp[:,:2] = np.mgrid[0:9,0:6].T.reshape(-1,2)
print ("step 2")

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
print ("step 3")

images = glob.glob('*.jpg')
print ("step 4")

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print("fname: ",fname)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
    print("ret: ",ret)

    # If found, add object points, image points (after refining them)
    if ret == True:
        cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners)
        objpoints.append(objp)
        
        # Draw and display the corners
        cv2.drawChessboardCorners(img, (9,6), corners, ret)
        cv2.imshow('grid',img)
        cv2.waitKey(500)
        
    else:
        print("none")
print ("step 5")

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
#np.savez("webcam_calibration_ouput_2", ret=ret, mtx=mtx, dist=dist, rvecs=rvecs, tvecs=tvecs)
print("step 6")
print ret
print mtx
print dist

img = cv2.imread('sikat8.jpg')
h,  w = img.shape[:2]
print(h)
print(w)
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

print newcameramtx
print roi
#cv2.imwrite('image.png',img)
print("step 7")



# undistort
#dst = cv2.undistort(img, mtx, dist, None, mtx)
dst = cv2.undistort(img, mtx, dist, None, newcameramtx)

np.savez("camcalib_1", mtx=mtx, dist=dist, newcameramtx=newcameramtx, roi=roi)

#mapx, mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
#dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
print("step 8")



# crop the image
x,y,w,h = roi #udah bisa, karena kurang data gambar 
print(x)
print(y)
print(w)
print(h)
dst = dst[y:y+h, x:x+w]
cv2.imwrite("undistort_.png",dst)
print("step 9")



