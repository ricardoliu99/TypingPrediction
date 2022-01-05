import tkinter as Tkinter
import numpy as np
import re
import json

def printInput(event):
    input = text_widget.get(1.0, Tkinter.INSERT)

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
            word1, word2, word3 = predictWordBi(lwd)
            updateLabels(word1, word2, word3)
        else:
            label.config(text = "Last 2 words: " + lwd2  + " " + lwd1)
            word1, word2, word3 = predictWordTri(lwd1, lwd2)
            updateLabels(word1, word2, word3)
    elif (len(str_arr) == 1):
        lwd, trim = strTrim(str_arr[-1])
        if (trim):
            clearLabels()
        else:
            label.config(text = "Last word: " + lwd)
            word1, word2, word3 = predictWordBi(lwd)
            updateLabels(word1, word2, word3)
    else:
        clearLabels()

def getWords(keys, vals):
    word2 = ''
    word3 = ''
    word1 = keys[np.argmax(vals)]
    vals[np.argmax(vals)] = 0
    if len(keys) > 1:
        word2 = keys[np.argmax(vals)]
        vals[np.argmax(vals)] = 0
    if len(keys) > 2:
        word3 = keys[np.argmax(vals)]
        vals[np.argmax(vals)] = 0
    return word1, word2, word3

def predictWordTri(lwd1, lwd2):
    word1 = ''
    word2 = ''
    word3 = ''
    lwd_k = lwd2 + " " + lwd1
    if lwd_k in trigram_counts:
        keys = list(trigram_counts[lwd_k].keys())
        vals = list(trigram_counts[lwd_k].values())
        word1, word2, word3 = getWords(keys, vals)
    if (word1 == '' or word2 == '' or word3 == ''):
        word1_1, word2_1, word3_1 = predictWordBi(lwd1)
        if (word1 == word1_1):
            word1 = ''
        if (word2 == word2_1):
            word2 = ''
        if (word3 == word3_1):
            word3 = ''
    if (word1 == ''):
        word1 = word1_1
    if (word2 == ''):
        word2 = word2_1
    if (word3 == ''):
        word3 = word3_1
    return word1, word2, word3

def predictWordBi(lwd):
    word1 = ''
    word2 = ''
    word3 = ''
    if lwd in bigram_counts:
        keys = list(bigram_counts[lwd].keys())
        vals = list(bigram_counts[lwd].values())
        word1, word2, word3 = getWords(keys, vals)
    return word1, word2, word3

def updateLabels(word1, word2, word3):
    wd1.config(text = word1)
    wd2.config(text = word2)
    wd3.config(text = word3)

def clearInput(event):
    clearLabels()

def insertWD(event, WD):
    text_widget.insert(Tkinter.INSERT, WD.cget("text") + " ")
    printInput(event)

def strTrim(str):
    trimmed = re.sub('\?|\.|\,|\!|\;|\:|\"|\—|\(|\)', '', str)
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

def loadModel(trigram, bigram):
    print("Loading model...")
    with open(trigram) as json_file_tri:
        trigram_result = json.load(json_file_tri)
    print("Trigram model loaded.")
    with open(bigram) as json_file_bi:
        bigram_result = json.load(json_file_bi)
    print("Bigram model loaded.")
    print("Starting GUI...")
    return trigram_result, bigram_result

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
text_widget.bind('<(>', clearLabelsEV)
text_widget.bind('<)>', clearLabelsEV)

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

trigram_counts, bigram_counts = loadModel('trigram_model.json', 'bigram_model.json')
Tkinter.mainloop()
