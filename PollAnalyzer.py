from OutputProducer import OutputProducer
from Student import Student
import pandas as pd
from Parser import Parser
import glob, os


class PollAnalyzer:
    __studentList = None
    __fileNames = None
    __answerKeys=None
    __attendanceData = None
    __myOutputProducer = None

    def __init__(self):

        self.__studentList=[]
        self.__fileNames=[]
        self.__attendanceData=[]
        self.__answerKeys=[]
        self.__myOutputProducer = OutputProducer.instance()
        self.__myOutputProducer.addIntoExecutionLog("System started!")

        path="./poll_files/"

        for file in glob.glob(path+"*.csv"):
            self.__fileNames.append(file)

        for file in glob.glob("*.xls"):
            if file != "studentList.XLS":
                self.__fileNames.append(file)

        parser = Parser()
        filePath = "./poll_files/studentList.XLS"
        self.__studentList = parser.parseStudentList(filePath)

        for file in self.__fileNames:
            att = parser.parseAttendance(file)
            self.__attendanceData.append(att)

        self.calculateAttendance()

        for file in self.__fileNames:
            parser.parseQuiz(file, self.__studentList)

        path="./poll_answers/"

        for file in glob.glob(path+"*.xls"):
            if file != "studentList.XLS":
                self.__answerKeys.append(file)


        for a in self.__answerKeys:
            parser.parseAnswerKey(a,self.__studentList)




    def getStudentList(self):
        return self.__studentList

    def calculateAttendance(self):

        num = 0

        for attendanceList in self.__attendanceData:

           if attendanceList!=None:
               num=num+1
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
        self.__studentList[0].setNumClasses(num)



    def calculateQuizResults(self):

        for studentList in self.__studentList:
            if studentList != None:
                fullUserNameList = []
                studentList = [x.lower() for x in studentList]

                for x in self.__studentList:
                    username = x.getName() + " " + x.getSurname()
                    fullUserNameList.append(username)

                for x in fullUserNameList:
                    x = x.lower()
                    if x in studentList:
                        stuIndex = self.getStuIndexWithUserName(x)
                        stuQuizes = self.__studentList[stuIndex].getQuizes()
                        quizPart = stuQuizes[stuIndex].getQuizParts()
                        for i in quizPart:
                            if i.getQuestion().getAnswer() == i.getStudentRespond():
                                x.increaseNumCorrect()
                            else:
                                x.increaseNumWrong()


    def getStuIndexWithUserName(self, username):

        for stu in self.__studentList:
            y = stu.getName() + " " + stu.getSurname()

            if y.lower() == username.lower():
                return self.__studentList.index(stu)

    def printStudentList(self):
        print(*self.__studentList, sep='\n')
