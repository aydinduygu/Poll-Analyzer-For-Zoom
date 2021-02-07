from tkinter import *
from tkinter.ttk import *
from tkinter import Label, ttk
from tkinter import filedialog
import tkinter as tk
from ttkthemes import ThemedStyle
import time
from PollAnalyzer import PollAnalyzer
import subprocess,os

class Gui():

    def __init__(self):

        self.root = Tk()

        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()

        self.root.geometry("660x340+" + str(int((width - 660) / 2)) + "+" + str(int((height - 340) / 2)))


        style = ThemedStyle(self.root)
        style.set_theme("radiance")
        a = 5

        self.a = False
        self.b = False
        self.c = False

        self.studentListPath = None

        textFrame=tk.Frame(self.root)
        textFrame.grid(row=0,column=0,sticky=E)
        self.text = Text(textFrame,height=3,width=73,bg=self.root["background"],relief=tk.FLAT,wrap="word",font="Ubuntu 12")
        self.text.insert(INSERT,"   Welcome to the Poll Analyzer! Load the student list, poll files and answer sheets")
        self.text.configure(state=DISABLED)
        self.text.tag_configure("right", justify="right")
        self.text.grid(pady=(20,0),padx=16,sticky=W+E+S)

        barFrame = tk.Frame(self.root)
        barFrame.grid(row=4, column=0, sticky="we", padx=20)
        self.bar = Progressbar(barFrame, orient=HORIZONTAL,length=597, mode="determinate", maximum=100)
        self.bar.grid(pady=20)

        startEndButFrame=tk.Frame(self.root)
        startEndButFrame.grid(row=5,column=0,sticky=E,padx=70)
        self.buttonEnd = Button(startEndButFrame, text="Cancel", command=self.cancel)
        self.buttonEnd.pack(side="right", padx=5, pady=5)
        self.buttonStart = Button(startEndButFrame, text="Start", command=self.start, state=DISABLED)
        self.buttonStart.pack(side="left",padx=5, pady=5)

        browseButFrame = tk.Frame(self.root)
        browseButFrame.grid(row=1, column=0, sticky=W + E + N)
        self.combo1 = ttk.Combobox(browseButFrame, height="10", width="63")
        self.combo1.grid(row=1, column=2)
        self.combo2 = ttk.Combobox(browseButFrame, height="10", width="63")
        self.combo2.grid(row=2, column=2)
        self.combo3 = ttk.Combobox(browseButFrame, height="10", width="63")
        self.combo3.grid(row=3, column=2)
        self.button_explore = Button(browseButFrame,text="Browse Student List",command=self.browseFiles)
        self.button_explore.grid(row=1,column=0,padx=5)
        self.button_explore2 = Button(browseButFrame,text="Browse Poll Reports",command=self.browseFiles2)
        self.button_explore2.grid(row=2,column=0, padx=20, pady=5)
        self.button_explore3 = Button(browseButFrame,text="Browse Answer Key",command=self.browseFiles3)
        self.button_explore3.grid(row=3,column=0, padx=20, pady=5)
        self.root.mainloop()


    def start(self):
        self.text.configure(state=NORMAL)
        self.text.delete(1.0,END)
        self.text.insert(INSERT,"Please wait! This may take a little time....")
        self.text.configure(state=DISABLED)
        self.text.grid(pady=(20, 0), padx=16, sticky=W + E + S)
        self.pollAnalyzer=PollAnalyzer(self, self.studentListPath, self.pollPath, self.answerPath)
        self.pollAnalyzer.start()

    def cancel(self):
        self.pollAnalyzer.stop()

    def browseFiles(self):
        self.studentListPath = filedialog.askopenfilename(initialdir="/",title="Select a File",
                                                           filetypes=(("Excel files","*.XLS*"),("all files","*.*")))
        self.combo1.insert(0,self.studentListPath)
        if self.studentListPath != None:
            self.a = True

        if self.a and self.b and self.c:
            self.buttonStart['state']=ACTIVE


    def browseFiles2(self):
        self.pollPath = []

        self.pollPath = filedialog.askopenfilenames(initialdir="/",title="Select a File",
                                                    filetypes=(("Excel files","*.csv*"),("all files", "*.*")))
        self.combo2.set(str(self.pollPath))
        if len(self.pollPath) != 0:
            self.b = True

        if self.a and self.b and self.c:

            self.buttonStart['state']=ACTIVE


    def browseFiles3(self):
        self.answerPath = []

        self.answerPath = filedialog.askopenfilenames(initialdir="/",title="Select a File",
                                                      filetypes=(("Text files","*.txt*"),("all files","*.*")))

        self.combo3.set(str(self.answerPath))
        if len(self.answerPath) != 0:
            self.c = True
        if self.a and self.b and self.c:

            self.buttonStart['state']=ACTIVE

    def updateBar(self, value):
        self.bar['value'] += value
        self.root.update_idletasks()
        time.sleep(1)
