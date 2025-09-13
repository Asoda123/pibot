import tkinter
from tkinter import *
from PIL import Image, EpsImagePlugin

height = 400
width = 700
zero_cords = (width/2,height/2)

USER_ID = None
def set_user_id(uid : int):
    global USER_ID
    USER_ID = str(uid)

EpsImagePlugin.gs_windows_binary = r"C:\Program Files\gs\gs10.05.1\bin\gswin64c.exe"
def create_lever(l1,l2):
    root = tkinter.Tk()
    first_length, second_length = l1*25, l2*25
    c = Canvas(root, width=width,height=height)
    c.pack()
    c.create_line(zero_cords[0] - first_length,zero_cords[1],zero_cords[0],zero_cords[1],
                  width=7,
                  fill='red')
    c.create_line(zero_cords[0] - first_length,zero_cords[1],zero_cords[0]-first_length, zero_cords[1]+100,
                  width=2)


    c.create_line(zero_cords[0] + second_length, zero_cords[1], zero_cords[0], zero_cords[1],
                  width=7,
                  fill='green')
    c.create_line(zero_cords[0] + second_length, zero_cords[1], zero_cords[0] + second_length, zero_cords[1] + 100,
                  width=2)

    c.create_rectangle(zero_cords[0]-first_length-second_length / 4, zero_cords[1]+100,
                       zero_cords[0]-first_length+second_length / 4, zero_cords[1]+100+second_length/2,
                       width=4,
                       fill='black')

    c.create_rectangle(zero_cords[0] + second_length - first_length / 4, zero_cords[1] + 100,
                       zero_cords[0] + second_length + first_length / 4, zero_cords[1] + 100 + first_length/2,
                       width=4,
                       fill='black')
    c.create_text(width/10,height/4, text=f'l1 = {l1} m\nl2 = {l2} m\nm1 = {l2} kg\nm2 = {l1} kg',font=('Impact', 20))

    root.update_idletasks()
    root.update()
    root.withdraw()

    temp_ps_name = f'temp_canv_{USER_ID}.ps'
    file_name = (f'canv_{USER_ID}.png')
    c.postscript(file=temp_ps_name,colormode='color')

    img = Image.open(temp_ps_name)

    img.save(file_name, 'png')