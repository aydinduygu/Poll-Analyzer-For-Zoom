from Student import Student
import pandas as pd
from Parser import Parser


class PollAnalyzer:
    __studentList = []

    def __init__(self):
        filePath1 = "CES3063_Fall2020_rptSinifListesi.XLS"
        filePath2 = "CSE3063_20201123_Mon_zoom_PollReport.csv"
        parser = Parser(filePath1, filePath2)
        self.__studentList = parser.parseStudentList()

        self.printStudentList()

    def getStudentList(self):
            return self.__studentList

    def printStudentList(self):
            print(*self.__studentList, sep='\n')