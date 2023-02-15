from tkinter import *


def create_window():
    
    def confirm():
        window.destroy() 
    window = Tk()
    submit = Button(window, text="Confirm", command=confirm)
    submit.pack(side=BOTTOM)
    L1 = Label(window, text="Rows to skip")
    L1.pack(side=LEFT)
    entry = Entry(window)
    entry.pack()
    entry.config(font=('Helvetica', 20), width=20)
    window.mainloop()
    
    
dab = create_window()
print(dab)