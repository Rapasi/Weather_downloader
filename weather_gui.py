import sqlite3 

# Using Tkinter for Gui
import tkinter as tk

#Importing weather_downnload function from weather_downnload.py
from weather import *

#Get users entry and show downloaded wether in label
def get_entry():
    try:
        weather=weather_downnload(entry.get())
        label2['text']=(f"{weather[0]}\n\n"
        f"Lämpötila {weather[1]}\u00b0C\n"
        f'Tuuli {weather[2]} m/s {degrees_to_cardinal(weather[3]) } ({myround(weather[3])}\u00b0)\n'
        f'Ilmanpaine {weather[4]} hPa\n'
        f'Lumen syvyys {weather[5]} \n')
    except Exception as e: 
        print(e)
        label2['text']='Syötä kelvollinen sijainti'

def get_sea():
    try:
        sea_level=sea_download(entry2.get())
        mittausasema=sea_download(entry2.get().capitalize())[1]
        for i in mittausasema:
            if i==entry2.get().capitalize():
                observation=i

        label2['text']=(f'Mittausasema {observation}\n'
        f'Vedenkorkeus on {sea_level[0]} cm')
    except Exception as e:
        print(e)
        label2['text']='Vedenkorkeus ei saatavilla valitulle paikalle'



# Usual Tkinter parameters
root=tk.Tk()
root.geometry('500x500')

label=tk.Label(root,text='Valitse paikka (sää)',fg='black',height=2)
label.place(relx=.1)

label2=tk.Label(root,text='Valitse paikka (vedenkorkeus)',fg='black',height=2)
label2.place(relx=.1,rely=.2)

entry=tk.Entry(root)
entry.place(anchor='center',relx=.2,rely=.1)

entry2=tk.Entry(root)
entry2.place(anchor='center',relx=.2,rely=.3)

button=tk.Button(root,text='Lataa säätiedot',command=lambda:get_entry())
button.place(anchor='center',relx=.5,rely=.1)

button2=tk.Button(root,text='Lataa vedenkorkeus',command=lambda:get_sea())
button2.place(anchor='center',relx=.5,rely=.3)


frame=tk.Frame(root,bd=10)
frame.place(relx=.4,rely=.5,anchor='n',relwidth=.75,relheight=.6)

label2=tk.Label(frame,font=("Arial", 16))
label2.place(relx=.02,rely=.1)


root.mainloop()
    
