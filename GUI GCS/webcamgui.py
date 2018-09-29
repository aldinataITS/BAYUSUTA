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

#width, height = 800, 600
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())

# Komponen penyusun tampilan, ada:
# - video (lmain_vid)
# - map (lmain_map)
# - informasi (lmain_info)
lmain_vid = tk.Label(root, relief=RIDGE)
lmain_map = tk.Label(text = 'Nanti peta di sini')
lmain_info = tk.Label(text = 'Data telemetri:\nLon=\nLat=',relief=RIDGE,justify=LEFT)

# Penempatan dengan metode grid
lmain_vid.grid(row=0, column = 0)
lmain_map.grid(row=0, column = 1)
lmain_info.grid(row=1, column = 0)

# Ambil video
def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain_vid.imgtk = imgtk
    lmain_vid.configure(image=imgtk)
    lmain_vid.after(10, show_frame)

show_frame()
root.mainloop()