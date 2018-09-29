# Trial Project
from tkinter import *
from PIL import ImageTk, Image

### main
window = Tk()
window.title("My Project")
### my photo
photo1 = ImageTk.PhotoImage(Image.open("bayucaraka.png"))
Label(window, image=photo1, bg="black").grid(row=0, column=0, sticky=E)

### run the main loop
window.mainloop()