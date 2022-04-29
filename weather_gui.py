import sqlite3 

# Using Tkinter for Gui
import tkinter as tk

#Importing weather_downnload function from weather_downnload.py
from weather import *

#Get users entry and show downloaded wether in label
def get_entry():
    try:
        weather=weather_downnload(entry_weather.get())
        label_data['text']=(f"{weather[0]}\n\n"
        f"Lämpötila {weather[1]}\u00b0C\n"
        f'Tuuli {weather[2]} m/s {degrees_to_cardinal(weather[3]) } ({myround(weather[3])}\u00b0)\n'
        f'Ilmanpaine {weather[4]} hPa\n'
        f'Pilvisyys {weather[6]}')
    except Exception as e: 
        print(e)
        label_data['text']='Tarkista sijainti'


# Converting user input in "sea" entry box to sea level output in frame. 

def get_sea():
    try:
        # Finding observation stations that correspond to user input. 
        sea_level=sea_download(entry_sea.get())
        observations=sea_download(entry_sea.get().capitalize())[1]
        for i in observations:
            if i==entry_sea.get().capitalize():
                observation=i

        label_data['text']=(f'Mittausasema{observation}\n'
        f'Vedenkorkeus on {sea_level[0]} cm')
    except Exception as e:
        print(e)
        label_data['text']='Vedenkorkeus ei saatavilla valitulle paikalle'



# Converting user input in metar entry box to metar output in frame. 

def get_metar():
    try:
        metar_data=metar_download(entry_metar.get())
        #label_data['font']=("Arial", 12)
        label_data['text']=metar_data.replace(' ','\n')
    
    # If no data is found for input data      
    
    except Exception as e:
        label_data['text']=('Ei saatavilla, tarkista syöte!\n'
        'Tarkista API avain weather.py koodissa.')

# Window size 

root=tk.Tk()
root.geometry('1000x1000')

# Labels that tell whitch entry box to input a location. 

label_weather=tk.Label(root,text='Valitse paikka (sää)',fg='black',height=2)
label_weather.place(relx=.05, rely=.05)

label_sea=tk.Label(root,text='Valitse paikka (vedenkorkeus)',fg='black',height=2)
label_sea.place(relx=.05,rely=.13)

label_metar=tk.Label(root,text='Valitse lentopaikka (ICAO)',fg='black',height=2)
label_metar.place(relx=.05,rely=.21)


# Entry boxes where user can input a derired location to download the data.  

entry_weather=tk.Entry(root)
entry_weather.place(anchor='center',relx=.2,rely=.1)

entry_sea=tk.Entry(root)
entry_sea.place(anchor='center',relx=.2,rely=.18)

entry_metar=tk.Entry(root)
entry_metar.place(anchor='center',relx=.2,rely=.26)


# Adding buttons that download requested data for entries. 

button=tk.Button(root,text='Lataa säätiedot',command=lambda:get_entry())
button.place(anchor='center',relx=.33,rely=.1)

button_sea=tk.Button(root,text='Lataa vedenkorkeus',command=lambda:get_sea())
button_sea.place(anchor='center',relx=.33,rely=.18)

button_metar=tk.Button(root,text='Lataa sää lentopaikalla',command=lambda:get_metar())
button_metar.place(anchor='center',relx=.33,rely=.26)

# Placing frame for diplaying the output 
frame=tk.Frame(root,bd=10)
frame.place(relx=.6,rely=.3,anchor='n',relwidth=.75,relheight=.6)

label_data=tk.Label(frame,font=("Arial", 16))
label_data.place(relx=.02,rely=.1)


root.mainloop()
    
