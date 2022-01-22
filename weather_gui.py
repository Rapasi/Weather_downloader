# Using Tkinter for Gui
import tkinter as tk

#Importing weather_downnload function from weather_downnload.py
from weather import weather_downnload

#Get users entry and show downloaded wether in label
def get_entry():
    weather=weather_downnload(entry.get())
    label2['text']=weather

# Usual Tkinter parameters
root=tk.Tk()
root.geometry('500x500')

label=tk.Label(root,text='Valitse paikka',fg='black',height=2)
label.place(relx=.1)

entry=tk.Entry(root)
entry.place(anchor='center',relx=.2,rely=.1)

button=tk.Button(root,text='Lataa säätiedot',command=lambda:get_entry())
button.place(anchor='center',relx=.5,rely=.1)

frame=tk.Frame(root,bd=10)
frame.place(relx=.4,rely=.2,anchor='n',relwidth=.75,relheight=.6)

label2=tk.Label(frame,font=("Arial", 16))
label2.place(relx=.02,rely=.1)

root.mainloop()