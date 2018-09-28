import numpy as np
import cv2
from math import radians,asin,sin,cos,tan,pi,degrees,atan2

#Loading Calibration Data
calibrationData = np.load('camcalib_3.npz')
mtx = calibrationData['mtx']
dist = calibrationData['dist']
newcameramtx = calibrationData['newcameramtx']
roi = calibrationData['roi']
#Close File
calibrationData.close()
#print mtx
#print dist
#print newcameramtx
#print roi
x,y,w,h = roi

#90%
w=576
h=432
x=32
y=24

#print x
#print y
#print w
#print h

cap = cv2.VideoCapture(0)

#Variable
rEarth = 6371.01 # Earth's average radius in km
#epsilon =  0.000001 # threshold for floating-point equality
latl = -7.2790319 #koordinat awal
lonl = 112.7900783  #koordinat awal
Sudut = 45.0 #Tergantung kemiringan pesawat
bearing = 0.0#arah pesawat utara (0) derajat
H = 25 #Ketinggian Pesawat (m)
var_y = 0.0848299134 #0.0547250929 #Perubahan sudut kamera terhadap sumbu y
var_x = 0.082723127 #0.0544879487 # Perubahan sudut kamera terhadap sumbu x

print"Ketinggian                 : ",H
print"Arah (Utara 0 Derajat)     : ",bearing
print"Sudut Kamera               : ",Sudut
print"latitude awal              : %.7f" % latl
print"longitude awal             : %.7f" % lonl
'''
def deg2rad(angle):
    return angle*pi/180


def rad2deg(angle):
    return angle*180/pi'''

def my_mouse_callback(event,x,y,flags,params):
    if event==cv2.EVENT_LBUTTONDOWN:
        x-=288
        y-=216
        y=y*(-1)
        #print "x: ",x
        #print "y: ",y
        D_suduty = var_y*y
        #print "Detlta sudut y: ", D_suduty
        D_sudutx = var_x*x
        #print "Detlta sudut y: ", D_sudutx
        sudut = Sudut+var_y*y #perubahan sudut
        #print "Sudut: ", sudut
        #print "Ketinggian: ", H
        J_pusat = H*tan(radians(Sudut)) #jarak titik pusat
        #print "Jarak pusat: ", J_pusat
        jarak_y = H*tan(radians(Sudut+var_y*y))
        #print "Jarak Terhadap Titik Tengah: ", jarak_y
        jarak_x = jarak_y/cos(radians(var_x*x))#jarak akhir
        #print "Jarak Akhir (m): ", jarak_x
        #print ""


        jarak_x = jarak_x/1000 #Mengubah jarak menjadi KM
        #print "Jarak Akhir (km): ", jarak_x
        rlat = radians(latl) #mengubah derajat menjadi radian
        #print"rlat: ",rlat
        rlon = radians(lonl) #mengubah derajat menjadi radian
        #print"rlon: ",rlon
        rbearing = radians(bearing+var_x*x) #mengubah derajat menjadi radian
        #print"rbearing: ",rbearing
        rdistance = jarak_x / rEarth # normalize linear distance to radian angle
        #print"rdistance: ",rdistance
        #print"rdistance # : %.7f" % rdistance

        nlat = asin( sin(rlat) * cos(rdistance) + cos(rlat) * sin(rdistance) * cos(rbearing) )
        #print"rlat #: ",nlat
        nlon = rlon + atan2(sin(rbearing)*sin(rdistance)*cos(rlat),cos(rdistance)-sin(rlat)*sin(nlat))
        #print"rlon #: ",nlon

        
        lat = degrees(nlat)
        lon = degrees(nlon)
        print"latitude tujuan            : %.7f" % lat
        print"longitude tujuan           : %.7f" % lon
        print"Jarak ke Koordinat Baru (m): ",jarak_x*1000

        
cv2.namedWindow("frame")
cv2.setMouseCallback('frame',my_mouse_callback)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame= cv2.undistort(frame, mtx, dist, None, newcameramtx)
    frame = frame[y:y+h, x:x+w]

    cv2.line(frame,(288,0),(288,432),(0,0,255),1)#vertikal
    cv2.line(frame,(0,216),(576,216),(0,0,255),1)#vertikal
        
    #print frame.shape
    # Display the resulting frame
    cv2.imshow('frame', frame) 
    
    #print(ret)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
