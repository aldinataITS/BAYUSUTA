 # Trial Project
from tkinter import *
from PIL import ImageTk, Image

# key down function
def click():
	entered__text = textentry.get() #it will collect the text from entry box
	output.delete(0.0, END)
	try:
		definition = my_compdictionary[entered__text]
	except:
		definition = "Sorry there is no word like that please try again"
	output.insert(END, definition)

def close_window():
	window.destroy()
	exit()

### main
window = Tk()
window.title("My Project")
window.configure(background="black")

### show photo
photo1 = ImageTk.PhotoImage(Image.open("bayucaraka.png"))
Label(window, image=photo1, bg="black").grid(row=0, column=0, sticky=W)

### create label
Label(window, text="Membuat label pada program", bg="white", fg="black", font="none 12 bold").grid(row=0, column=1, sticky=W)

### create a text entry box
textentry = Entry(window, width=20, bg="white")
textentry.grid(row=1, column=1, sticky=W)

### add a submit button
Button(window, text="SUBMIT", width=6, command=click).grid(row=2, column=1, sticky=W)

### create another label
Label(window, text="Label ke-2", bg="white", fg="black", font="none 12 bold").grid(row=3, column=0, sticky=W)

### create a text box
output = Text(window, width=75, height=6, wrap=WORD, bg="white")
output.grid(row=4, column=0, columnspan=2, sticky=W)

### the dictionary
my_compdictionary = {
	'algorithm': 'Step by step instructions to complete a task',
	'bug': 'piece of code that causes a program to fail'
}

### exit label
Label(window, text="click to exit", bg="black", fg="white", font="none 12 bold").grid(row=5, column=0, sticky=W)
Button(window, text="EXIT", width=14, command=close_window).grid(row=6, column=0, sticky=W)


### run the main loop
window.mainloop()