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

        att = parser.attendance(filePath2)

        print(att)

        self.printStudentList()

    def getStudentList(self):
        return self.__studentList

    def calculateAttendance(self, attendanceList):

        fullUserNameList = []

        for x in self.__studentList:
            username = x.getName() + " " + x.getSurname();
            fullUserNameList.append(username)

        for x in fullUserNameList:
            x = x.lower()
            if x in attendanceList:
                stu = self.getStuWithUserName(x)
                stu.increaseAttendance()

    def getStuWithUserName(self, username):

        for x in self.__studentList:
            y = x.getName + " " + x.getSurname

            if x.lower() == username.lower():
                return x

    def printStudentList(self):
        print(*self.__studentList, sep='\n')
