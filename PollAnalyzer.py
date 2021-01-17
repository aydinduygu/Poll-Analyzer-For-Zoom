from OutputProducer import OutputProducer
from Student import Student
import pandas as pd
from Parser import Parser
import glob, os


class PollAnalyzer:
    __studentList = []
    __fileNames = []
    __attendanceData = []
    __myOutputProducer = None

    def __init__(self):

        self.__myOutputProducer = OutputProducer.instance()
        self.__myOutputProducer.addIntoExecutionLog("System started!")
        os.chdir("poll_files")
        for file in glob.glob("*.csv"):
            self.__fileNames.append(file)

        for file in glob.glob("*.xls"):
            if file != "studentList.XLS":
                self.__fileNames.append(file)

        parser = Parser()
        filePath = "studentList.XLS"
        self.__studentList = parser.parseStudentList(filePath)

        for file in self.__fileNames:
            att = parser.parseAttendance(file)
            self.__attendanceData.append(att)

        self.calculateAttendance()
        parser.parseQuiz(self.__fileNames[0], self.__studentList)

        self.printStudentList()



    def getStudentList(self):
        return self.__studentList

    def calculateAttendance(self):

        for attendanceList in self.__attendanceData:
            fullUserNameList = []
            attendanceList = [x.lower() for x in attendanceList]

            for x in self.__studentList:
                username = x.getName() + " " + x.getSurname()
                fullUserNameList.append(username)

            for x in fullUserNameList:
                x = x.lower()
                if x in attendanceList:
                    stuIndex = self.getStuIndexWithUserName(x)
                    self.__studentList[stuIndex].increaseAttendance()

    def getStuIndexWithUserName(self, username):

        for stu in self.__studentList:
            y = stu.getName() + " " + stu.getSurname()

            if y.lower() == username.lower():
                return self.__studentList.index(stu)

    def printStudentList(self):
        print(*self.__studentList, sep='\n')