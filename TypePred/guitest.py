import tkinter as Tkinter
import numpy as np
import re

def printInput(event):
    input = text_widget.get(1.0,Tkinter.INSERT)

    cur_len = len(input)
    if (cur_len > 30):
        input = input[(cur_len - 30):]

    str_arr = input.split()
    if (len(str_arr) >= 2):
        lwd1, trim1 = strTrim(str_arr[-1])
        lwd2, trim2 = strTrim(str_arr[-2])
        if (trim1):
            clearLabels()
        elif (trim2):
            label.config(text = "Last word: " + lwd1)
            predictWordBi(lwd1)
        else:
            label.config(text = "Last 2 words: " + lwd2  + " " + lwd1)
            predictWordTri(lwd1, lwd2)
    elif (len(str_arr) == 1):
        lwd, trim = strTrim(str_arr[-1])
        if (trim):
            clearLabels()
        else:
            label.config(text = "Last word: " + lwd)
            predictWordBi(lwd)
    else:
        clearLabels()

def predictWordTri(lwd1, lwd2):
    wd1.config(text =  arr[np.random.randint(0, 7)])
    wd2.config(text =  arr[np.random.randint(0, 7)])
    wd3.config(text =  arr[np.random.randint(0, 7)])

def predictWordBi(lwd):
    wd1.config(text =  arr[np.random.randint(0, 7)])
    wd2.config(text =  arr[np.random.randint(0, 7)])
    wd3.config(text =  arr[np.random.randint(0, 7)])

def clearInput(event):
    clearLabels()

def insertWD(event, WD):
    text_widget.insert(Tkinter.INSERT, WD.cget("text"))

def strTrim(str):
    trimmed = re.sub('\?|\.|\,|\!|\;|\:|\"|\—', '', str)
    if len(trimmed) != len(str):
        return trimmed, 1
    return str, 0

def clearLabels():
    label.config(text = "")
    wd1.config(text = "")
    wd2.config(text = "")
    wd3.config(text = "")

def clearLabelsEV(event):
    clearLabels()

parent_widget = Tkinter.Tk()
parent_widget.title("Typing Prediction GUI Test")
parent_widget.minsize(width = 500, height = 500)

text_widget = Tkinter.Text(parent_widget, font = ("Consolas", 12))
text_widget.pack(fill = "both", expand = True)
text_widget.bind('<space>', printInput)
text_widget.bind('<BackSpace>', clearInput)
text_widget.bind('<?>', clearLabelsEV)
text_widget.bind('<.>', clearLabelsEV)
text_widget.bind('<,>', clearLabelsEV)
text_widget.bind('<!>', clearLabelsEV)
text_widget.bind('<;>', clearLabelsEV)
text_widget.bind('<:>', clearLabelsEV)
text_widget.bind('<">', clearLabelsEV)

label = Tkinter.Label(parent_widget, text = "", font = ("Consolas", 12))
label.pack(side = Tkinter.TOP)

wd1 = Tkinter.Label(parent_widget, text = "", font = ("Consolas", 12), relief="solid")
wd1.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH, expand = 1)
wd1.bind('<Button-1>', lambda event, WD = wd1: insertWD(event, wd1))
wd2 = Tkinter.Label(parent_widget, text = "", font = ("Consolas", 12), relief="solid")
wd2.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH, expand = 1)
wd2.bind('<Button-1>', lambda event, WD = wd2: insertWD(event, wd2))
wd3 = Tkinter.Label(parent_widget, text = "", font = ("Consolas", 12), relief="solid")
wd3.pack(side = Tkinter.LEFT, fill = Tkinter.BOTH, expand = 1)
wd3.bind('<Button-1>', lambda event, WD = wd3: insertWD(event, wd3))

arr = ["000000", "111111", "222222", "333333", "444444", "555555", "666666"]

Tkinter.mainloop()
