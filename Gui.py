from tkinter import *
from tkinter.ttk import *
from tkinter import Text
from tkinter import Label
from tkinter import filedialog
import time
from PollAnalyzer import PollAnalyzer


class Gui():

    def __init__(self):
        a=5

        self.window = Tk()
        self.window.title("Poll Analyzer")

        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()

        self.window.geometry("750x300+" + str(int((width - 750) / 2)) + "+" + str(int((height - 300) / 2)))

        self.lbl = Label(self.window,
                         text="Welcome to the Poll Analyzer,\nPut csv files into the directory 'poll_files' \nAnd answer txt files into poll_answers directories\nPress Start to analyze poll results",
                         font=("Arial", 10)).pack(pady=20)
        self.bar = Progressbar(self.window, orient=HORIZONTAL, length=350,mode="determinate",maximum=100)
        self.bar.pack(pady=10)

        buttonEnd = Button(self.window, text="Cancel", command=self.cancel).pack(side=RIGHT, padx=15, pady=5)
        buttonStart = Button(self.window, text="Start", command=self.start).pack(side=RIGHT, padx=5, pady=5)
        button_explore = Button(self.window,
                                text="Browse Student List",
                                command=self.browseFiles).pack(side=LEFT, padx=20, pady=5)
        button_explore2 = Button(self.window,
                                 text="Browse Poll Reports",
                                 command=self.browseFiles2).pack(side=LEFT, padx=20, pady=5)
        button_explore3 = Button(self.window,
                                 text="Browse Answer Key",
                                 command=self.browseFiles3).pack(side=LEFT, padx=20, pady=5)
        self.window.mainloop()

    def start(self):
        self.window.configure()

        self.lbl = Label(self.window, text="Please wait... This may take a little time")

        PollAnalyzer(self,self.studentListPath,self.pollPath,self.answerPath)

    def cancel(self):
        exit()

    def browseFiles(self):
        self.studentListPath = filedialog.askopenfilename(initialdir="/",
                                                     title="Select a File",
                                                     filetypes=(("Excel files",
                                                                 "*.XLS*"),
                                                                ("all files",
                                                                 "*.*")))

    def browseFiles2(self):

        self.pollPath=[]

        self.pollPath = filedialog.askopenfilenames(initialdir="/",
                                              title="Select a File",
                                              filetypes=(("Excel files",
                                                          "*.csv*"),
                                                         ("all files",
                                                          "*.*")))


    def browseFiles3(self):

        self.answerPath=[]
        self.answerPath = filedialog.askopenfilenames(initialdir="/",
                                                title="Select a File",
                                                filetypes=(("Text files",
                                                            "*.txt*"),
                                                           ("all files",
                                                            "*.*")))


    def updateBar(self,value):


        self.bar['value']+=value
        self.window.update_idletasks()
        time.sleep(1)