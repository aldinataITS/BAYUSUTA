'''
### Rotating Image with PIL
from PIL import Image
image = Image.open('Audi.jpg')
# rotate 270 degrees counter-clockwise
imRotate = image.rotate(270)
filename = "AudiRotated2.jpg"
imRotate.save(filename)
# a simple way to show the image file is to use module webbrowser
# which activates the default viewer associated with the image
# works with Windows and Linux
import webbrowser
webbrowser.open(filename)'''
'''
### Font Style
myFont = Font(family="Times New Roman", size=12)
text.configure(font=myFont)

text.configure(font=("Times New Roman", 12, "bold"))
'''

#import tkinter as tk
from tkinter import *
import ttk
import numpy as np
import cv2
from PIL import Image, ImageTk



root = Tk()
root.resizable(width=FALSE,height=FALSE)
root.title("Bayusuta")
#root.pack(fill=BOTH,expand=True)

#Mekanisme:
#Tentukan default size windownya jika tidak fullscreen
#Bagaimana membuat gambar bergerak atau rotasi ++
#membuat list waypoint ++
#mengganti font style ++
#tkinter event: click, double click++

# Komponen penyusun tampilan, ada:
# Logo (wd_logo) +++
# Connect/Disconnect Button, Baud, FC version (wd_connect)
# - video (wd_video) +++
# - map (wd_maps)
# - Status Pesawat (wd_stat)
# Action: Arm, Mode dll
# Flight Visual (wd_visual) // Optional
# Flight Plan (wd_plan)

#------LOGO--------
#logo.create_rectangle(0,0,374,100,fill='red')
photo1 = ImageTk.PhotoImage(Image.open("td.png"))
logo = Label(image=photo1)


#-----CAMERA--------
cam = Canvas(root,width=374,height=280)#374,280
#cam.create_rectangle(0,0,374,280,fill='green')
vid = Label(cam, relief=RIDGE)
vid.pack()

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
#resize camera
width = int(576*65/100)
height = int(432*65/100)
dim = (width, height)

cap = cv2.VideoCapture(0)
def showFrame():
    _, frame = cap.read()
    frame= cv2.undistort(frame, mtx, dist, None, newcameramtx)
    frame = frame[y:y+h, x:x+w]
    #cv2.line(frame,(288,0),(288,432),(0,0,255),1)   # garis vertikal
    #cv2.line(frame,(0,216),(576,216),(0,0,255),1)   # garis horisontal
    frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)
    cv2.line(frame,(187,0),(187,280),(0,0,255),1) #Vertical
    cv2.line(frame,(0,140),(574,140),(0,0,255),1) #Horizontal
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    vid.imgtk = imgtk
    vid.configure(image=imgtk)
    vid.after(10, showFrame)


#------TAB----------
tab = Canvas(root)#,width=374,height=260)
#tab.create_rectangle(0,0,374,260,fill='red')
tabControl = ttk.Notebook(tab)
action = ttk.Frame(tabControl,width=374,height=230)
tabControl.add(action, text="Action")
status = ttk.Frame(tabControl,width=374,height=230)
tabControl.add(status, text="Status")
fVisual = ttk.Frame(tabControl,width=374,height=230)
tabControl.add(fVisual, text="Fligt Visual")
fPlan = ttk.Frame(tabControl,width=374,height=230)
tabControl.add(fPlan, text="Fligt Plan")

tabControl.pack(expand=True,fill=BOTH)

#Action
a1 = Canvas(action,width=370,height=230)
#a1.create_rectangle(0,0,100,100,fill='red')

#-version_connect-
statVer = Label(action,text="0",width=2,borderwidth=1,relief='solid')
statVer.place(x=8,y=10)#48
version = Label(action,text="",width=30,borderwidth=1,relief='solid')
version.place(x=35,y=10)
#-Port_connect-
portList = ["AUTO", "TCP", "UDP", "UDPCI"]
selectedPort = StringVar()
selectedPort.set(portList[0])
portMenu = OptionMenu(action,selectedPort, *portList)
portMenu.config(width=12)
portMenu.place(x=5,y=32)
#-Baud_connect-
baudList = ["9600","57600","115200"]
selectedBaud = StringVar()
selectedBaud.set(baudList[0])
baudMenu = OptionMenu(action,selectedBaud, *baudList)
baudMenu.config(width=8)
baudMenu.place(x=120,y=32)
#-connect_connect-
connectbtn = Button(action,text="Connect",width=12)#connected
connectbtn.place(x=240,y=35)

#-stat_mode-
statVer = Label(action,text="0",width=2,borderwidth=1,relief='solid')
statVer.place(x=8,y=80)#48
version = Label(action,text="Mode :",width=30,borderwidth=1,relief='solid')
version.place(x=35,y=80)
#-mode_mode-
modeList = ["AUTO","Guided","Stabilize"]
selectedMode = StringVar()
selectedMode.set(modeList[0])
modeMenu = OptionMenu(action,selectedMode, *modeList)
modeMenu.config(width=12)
modeMenu.place(x=5,y=102)
#-set_mode-
modebtn = Button(action,text="Set Mode",width=12)
modebtn.place(x=145,y=105)

#-action_action-
actionList = ["Loiter","RTL","Preflight Calibration","Start Mission"]
selectedAction = StringVar()
selectedAction.set(actionList[0])
actionMenu = OptionMenu(action,selectedAction, *actionList)
actionMenu.config(width=18)
actionMenu.place(x=5,y=150)
#-do_action-
actionbtn = Button(action,text="Do Action",width=12)
actionbtn.place(x=180,y=150)

a1.pack()
#ttk.Label(a1)
tabControl.pack()




#--------MAPS---------
maps = Canvas(root, width=640,height=640)
maps.create_rectangle(0,0,640,640,fill='blue')


#------PLACEMENT-------
logo.grid()
cam.grid(row=1,column=0)
tab.grid(row=2,column=0)
maps.grid(row=0,column=1,rowspan=3)


root.geometry("1020x645")
showFrame()
root.mainloop()
cap.release()


