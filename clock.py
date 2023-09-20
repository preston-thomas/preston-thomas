from tkinter import *
from time import strftime

# creates and titles window for our clock
clock_window = Tk()
clock_window.title('Digital Clock')


# manages the time aspect of the clock, updating every 1000ms
def time():
    current_time = strftime('%I:%M:%S %p')
    my_time.config(text=current_time)
    my_time.after(1000, time)

# manages the date aspect of the clock, also updating every 1000ms
def date():
    current_date = strftime('%Y-%m-%d')
    my_date.config(text=current_date)
    my_date.after(1000, date)

# formats the clock to my liking
my_time = Label(clock_window, font=('helvect', 50, 'bold'), background='purple', foreground='white')
my_time.grid(row=1, column=0, padx=10, pady=10)

my_date = Label(clock_window, font=('helvecta', 20), background='purple', foreground='white')
my_date.grid(row=0, column=0, padx=10, pady=10)

time()
date()

mainloop()
