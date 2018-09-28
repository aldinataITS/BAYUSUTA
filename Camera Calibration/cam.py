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
print mtx
print dist
print newcameramtx
print roi
x,y,w,h = roi

#90%
w=576
h=432
x=32
y=24

print x
print y
print w
print h

#resize
width = int(576*111/100)
height = int(432*111/100)
dim = (width, height)

cap = cv2.VideoCapture(0)

#Variable
rEarth = 6371.01 # Earth's average radius in km
epsilon =  0.000001 # threshold for floating-point equality
latl = 0#-7.2790319 #koordinat awal
lonl = 0#112.7900783  #koordinat awal
print"latl: ",latl
print"lonl: ",lonl
Sudut = 30.0 #Tergantung kemiringan pesawat
bearing = 90.0#arah pesawat utara (0) derajat
H = 25 #Ketinggian Pesawat (m)
var_y = 0.0848299134 #0.0547250929 #Perubahan sudut kamera terhadap sumbu y
var_x = 0.082723127 #0.0544879487 # Perubahan sudut kamera terhadap sumbu x

def deg2rad(angle):
    return angle*pi/180


def rad2deg(angle):
    return angle*180/pi

def my_mouse_callback(event,x,y,flags,params):
    if event==cv2.EVENT_LBUTTONDOWN:
        x-=288
        y-=216
        y=y*(-1)
        print "x: ",x
        print "y: ",y
        D_suduty = var_y*y
        print "Detlta sudut y: ", D_suduty
        D_sudutx = var_x*x
        print "Detlta sudut y: ", D_sudutx
        sudut = Sudut+var_y*y
        print "Sudut: ", sudut
        print "Ketinggian: ", H
        J_pusat = H*tan(deg2rad(Sudut))
        print "Jarak pusat: ", J_pusat
        jarak_y = H*tan(radians(Sudut+var_y*y))#
        print "Jarak Terhadap Titik Tengah: ", jarak_y
        jarak_x = jarak_y/cos(radians(var_x*x))#
        print "Jarak Akhir (m): ", jarak_x
        print ""


        jarak_x = jarak_x/1000
        print "Jarak Akhir (km): ", jarak_x
        rlat = deg2rad(latl)
        rlon = deg2rad(lonl)
        rbearing = deg2rad(bearing+var_x*x)
        rdistance = jarak_x / rEarth # normalize linear distance to radian angle
        print"rlat: ",rlat
        print"rlon: ",rlon
        print"rbearing: ",rbearing
        print"rdistance: ",rdistance
        print"rdistance # : %.14f" % rdistance

        #lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
        nilai = cos(rlat) * sin(rdistance) * cos(rbearing)
        print "nilai: ",nilai
        nilai1 = cos(rbearing*pi/180)
        print "nilai1: ",nilai1
        nlat = asin( sin(rlat) * cos(rdistance) + cos(rlat) * sin(rdistance) * cos(rbearing) )
        print"rlat #: ",nlat

        nlon = rlon + atan2(sin(rbearing)*sin(rdistance)*cos(rlat),cos(rdistance)-sin(rlat)*sin(nlat))
        print"rlon #: ",nlon

        
        lat = rad2deg(nlat) ## masih gagal
        lon = rad2deg(nlon)
        print"lat : %.7f" % lat
        print"lon : %.7f" % lon

        
cv2.namedWindow("frame")
cv2.setMouseCallback('frame',my_mouse_callback)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame= cv2.undistort(frame, mtx, dist, None, newcameramtx)
    frame = frame[y:y+h, x:x+w]
    #frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    '''
    #cv2.line(frame, (0,40), (640,40), (0,0,0), 1) # horisontal 2.5
    cv2.line(frame, (0,80), (640,80), (0,0,0), 1) # horisontal 2
    #cv2.line(frame, (0,120), (640,120), (0,0,0), 1)# horisontal 1.5
    cv2.line(frame, (0,160), (640,160), (0,0,0), 1)# horisontal 1
    #cv2.line(frame, (0,200), (640,200), (0,0,0), 1) #tengah horisontal 0.5
    cv2.line(frame, (0,240), (640,240), (0,0,255), 1) #tengah horisontal 0
    #cv2.line(frame, (0,280), (640,280), (0,0,0), 1) #tengah horisontal -0.5
    cv2.line(frame, (0,320), (640,320), (0,0,0), 1) #horisontal -1
    #cv2.line(frame, (0,360), (640,360), (0,0,0), 1) #horisontal -1.5
    cv2.line(frame, (0,400), (640,400), (0,0,0), 1) #horisontal -2
    #cv2.line(frame, (0,440), (640,440), (0,0,0), 1) #horisontal -2.5
    
    #cv2.line(frame, (40,0), (40,480), (0,0,0), 1) #vertikal -3.5
    cv2.line(frame, (80,0), (80,480), (0,0,0), 1) #vertikal -3
    #cv2.line(frame, (120,0), (120,480), (0,0,0), 1) #vertikal -2.5
    cv2.line(frame, (160,0), (160,480), (0,0,0), 1) #vertikal -2
    #cv2.line(frame, (200,0), (200,480), (0,0,0), 1) #vertikal -1.5
    cv2.line(frame, (240,0), (240,480), (0,0,0), 1) #vertikal -1
    #cv2.line(frame, (280,0), (280,480), (0,0,0), 1) #tengah vertikal -0.5
    cv2.line(frame, (320,0), (320,480), (0,0,255), 1) #tengah vertikal 0
    #cv2.line(frame, (360,0), (360,480), (0,0,0), 1) #tengah vertikal 0.5
    cv2.line(frame, (400,0), (400,480), (0,0,0), 1) #vertikal 1
    #cv2.line(frame, (440,0), (440,480), (0,0,0), 1) #vertikal 1.5
    cv2.line(frame, (480,0), (480,480), (0,0,0), 1) #vertikal 2
    #cv2.line(frame, (520,0), (520,480), (0,0,0), 1) #vertikal 2.5
    cv2.line(frame, (560,0), (560,480), (0,0,0), 1) #vertikal 3
    #cv2.line(frame, (600,0), (600,480), (0,0,0), 1) #vertikal 3.5'''
    

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
