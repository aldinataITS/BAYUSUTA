# webcamgui.py
# Menggabungkan tampilan dari webcam dll ke dalam window tunggal,
# menggunakan Tkinter.
# Tim TD Bayusuta dan Irfan, 2018

# Di laptop saya (irfan), saya pakai python 3.6
import tkinter as tk
from tkinter import *
# Kalau pakai pyton 2.7 mungkin agak beda?
# import Tkinter as tk
#from Tkinter import *
import cv2
from PIL import Image, ImageTk
import math
from urllib.request import urlopen
import numpy as np
from math import radians,asin,sin,cos,tan,pi,degrees,atan2

#------ data pesawat
lat = -7.2833138    # Latitude
lon = 112.8099354       # Longitude
latl = -7.2790319 #koordinat awal
lonl = 112.7900783  #koordinat awal
z = 15  # Zoom level

#------ menerjemahkan koordinat GPS lat, lon ke x, y tile yang disediakan HERE maps.
def compute_map_tile(lat, lon, z):
    latRad = lat * math.pi / 180
    n = math.pow(2, z)
    xTile = n * ((lon + 180) / 360)
    yTile = n * (1-(math.log(math.tan(latRad) + 1/math.cos(latRad)) /math.pi)) / 2
    xTile = int(xTile)
    yTile = int(yTile)
    return xTile, yTile


#-------- Loading Calibration Data (dari fixcam.py per 30 Sept 2018)
calibrationData = np.load('camcalib_3.npz')
mtx = calibrationData['mtx']
dist = calibrationData['dist']
newcameramtx = calibrationData['newcameramtx']
roi = calibrationData['roi']
calibrationData.close()
x,y,w,h = roi

#90%
w=576
h=432
x=32
y=24

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

print("Ketinggian                 : "+str(H))
print("Arah (Utara 0 Derajat)     : "+str(bearing))
print("Sudut Kamera               : "+str(Sudut))
print('latitude awal              : %.7f' % latl)
print('longitude awal             : %.7f' % lonl)

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
        print('latitude tujuan            : %.7f' % lat)
        print('longitude tujuan           : %.7f' % lon)
        print('Jarak ke Koordinat Baru (m): '+str(jarak_x*1000))
        
#cv2.namedWindow("frame")
#cv2.setMouseCallback('frame',my_mouse_callback)

# ########## START PROGRAM UTAMA #################

#------- Tes baca gambar peta
xtile, ytile = compute_map_tile(latl, lonl, z)
url = 'https://1.aerial.maps.api.here.com/maptile/2.1/maptile/newest/hybrid.day/'+str(z)+'/'+str(xtile)+'/'+str(ytile)+'/512/png8?app_id=juUPsCmrwzrj7aPjyUMr&app_code=z4cqdxfPNMQha0k89L0-TA'
#print(url)
with urlopen(url) as handle:
    data_photo = handle.read()


#------- Inisialisasi objek cap untuk baca webcam/video receiver USB
#width, height = 800, 600
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#-------- Inisialisasi GUI dengan Tkinter
root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
root.title('Bayusuta Ground Control Station')

# Baca file logo dan map
photo1 = ImageTk.PhotoImage(Image.open("bayucaraka.png"))
im = tk.PhotoImage(master=root, data=data_photo)

# Komponen penyusun tampilan, ada:
# - video (lmain_vid)
# - map (lmain_map)
# - informasi (lmain_info)
lmain_vid = tk.Label(root, relief=RIDGE)
#lmain_map = tk.Label(text = 'Nanti peta di sini')
lmain_map = tk.Label(image = im)
lmain_info = tk.Label(text = 'Data telemetri:\nLon=\nLat=',relief=RIDGE,justify=LEFT, font=("Courier", 16))
lmain_logo = tk.Label(image=photo1, bg="black")


# Penempatan dengan metode grid
lmain_vid.grid(sticky="N", row=0, column = 0)
lmain_map.grid(row=0, column = 1)
lmain_info.grid(sticky="NW", row=1, column = 0)
lmain_logo.grid(sticky="E", row=1, column = 1)

# Ambil video
def show_frame():
 
    #------ update video
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)

    # Didatarkan
    frame= cv2.undistort(frame, mtx, dist, None, newcameramtx)
    frame = frame[y:y+h, x:x+w]
    # Tambah garis
    cv2.line(frame,(288,0),(288,432),(0,0,255),1)   # garis vertikal
    cv2.line(frame,(0,216),(576,216),(0,0,255),1)   # garis horisontal

    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain_vid.imgtk = imgtk
    lmain_vid.configure(image=imgtk)
    lmain_vid.after(10, show_frame)     # ini artinya apa ya?
    
    #------ update teks informasi
    global lonl
    lonl = lonl - 0.0001
    info_text = 'INFORMASI\n=========\nKetinggian                 : '+str(H)+'\nArah (Utara 0 Derajat)     : '+str(bearing)+'\nSudut Kamera               : '+str(Sudut)+'\nLatitude UAV               : %.7f\nLongitude UAV              : %.7f' % (lonl, latl)
    lmain_info.configure(text = info_text, font=("Courier", 16))    

    # ----- update maps seperlunya saja (masih kasar ini)
    xtile1, ytile1 = compute_map_tile(latl, lonl, z)
    global xtile
    global ytile
    if ((xtile != xtile1) | (ytile != ytile1)):
        print('Update map')
        xtile = xtile1
        ytile = ytile1
        url = 'https://1.aerial.maps.api.here.com/maptile/2.1/maptile/newest/hybrid.day/'+str(z)+'/'+str(xtile)+'/'+str(ytile)+'/512/png8?app_id=juUPsCmrwzrj7aPjyUMr&app_code=z4cqdxfPNMQha0k89L0-TA'
        with urlopen(url) as handle:
            data_photo = handle.read()
        imgg = tk.PhotoImage(data=data_photo)
        lmain_map.imgtk = imgg
        lmain_map.configure(image = imgg)

show_frame()
root.mainloop()
