from tkinter import *
from tkinter.ttk import *
from tkinter import Text
from tkinter import Label
import time
from PollAnalyzer import PollAnalyzer

class Gui():


    def __init__(self):
        self.window = Tk()
        self.window.title("Poll Analyzer")

        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()

        self.window.geometry("500x200+"+str(int((width-500)/2))+"+"+str(int((height-200)/2)))

        self.lbl = Label(self.window, text="Welcome to the Poll Analyzer,\nPut csv files into the directory 'poll_files' \nAnd answer txt files into poll_answers directories\nPress Start to analyze poll results" , font=("Arial", 10)).pack(pady=20)
        bar = Progressbar(self.window, orient=HORIZONTAL, length=350)
        bar.pack(pady=10)

        buttonEnd = Button(self.window, text="Cancel",command=self.cancel).pack(side=RIGHT, padx=15, pady=5)
        buttonStart = Button(self.window, text="Start", command=self.start).pack(side=RIGHT,padx=5,pady=5)

        self.window.mainloop()

    def start(self):
        
        self.window.configure()

        self.lbl=Label(self.window,text="Please wait... This may take a little time")

        PollAnalyzer()


    def cancel(self):

        exit()




