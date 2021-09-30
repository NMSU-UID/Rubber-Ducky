# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 22:43:27 2021

@author: Owner
"""

import tkinter as tk;

i=0
window = tk.Tk();

label = tk.Label(window, text="Hello world.\n\tWhat's up with you?");
label.grid(column=0, row=0);

window.geometry('550x200')



def clicked():
    global i
    btn.configure(text="Yay! you clicked me. Click again")
    btn.grid(column=1,row=3)
    print("value of " + str(i) +".")
    i = i+1
    if (i > 3):
        btn2=tk.Button(window, text="Okay, time to go", command=window.destroy)
        btn2.grid(column=2,row=3)
        
btn = tk.Button(window, text='click here!', command = clicked)
btn.grid(column=1,row=3)




window.mainloop();