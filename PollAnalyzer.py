from OutputProducer import OutputProducer
from Parser import Parser
import glob, os
from QuestionStat import QuestionStat
from QuizStat import QuizStat

class PollAnalyzer:
    __studentList = None
    __fileNames = None
    __answerKeys=None
    __attendanceData = None
    __myOutputProducer = None
    __pollList=None


    def __init__(self):

        self.__studentList=[]
        self.__fileNames=[]
        self.__attendanceData=[]
        self.__answerKeys=[]
        self.__myOutputProducer = OutputProducer.instance()
        self.__myOutputProducer.addIntoExecutionLog("System started!")
        self.__pollList={}
        self.__dataNotCorrelated={}
        self.__stuNotCorrelated=[]


        path=".\poll_files"
        path2=".\poll_answers"

        for file in glob.glob(path+r"/*.csv"):


            self.__fileNames.append(file)

            print(file)
        for file in glob.glob("*.xls"):
            if file != "studentList.XLS":
                self.__fileNames.append(file)

        for file in glob.glob(path2+r"/*.txt"):
            self.__answerKeys.append(file)

        filePath = "./poll_files/studentList.XLS"

        columnNames={"name":"Adı","surname":"Soyadı","id":"Öğrenci No","username":"User Name","email":"User Email","datetime":"Submitted Date/Time"}

        parser = Parser(filePath, self.__fileNames, self.__answerKeys, columnNames)


        self.__studentList,self.__dataNotCorrelated,self.__stuNotCorrelated=parser.parse(filePath,self.__fileNames,columnNames,self.__answerKeys)


        self.calculateQuizStats()

        self.__myOutputProducer.printPollStat(self.__pollList)


        self.__myOutputProducer.printAttendenceReport(self.__studentList)
        self.__myOutputProducer.printPollResults(self.__studentList,self.__pollList)
        self.__myOutputProducer.printStudentOverallResults(self.__studentList,self.__pollList)


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
                       self.__studentList[stuIndex].setNumClasses(num)







    def calcQuestionStat(self):

        i=0
        for key in self.__pollList:

            questions=[x.getQuestion().getQuestionText() for x in self.__pollList[key][0].getQuizes()[i].getQuizParts()
                       if self.__pollList[key][0].getQuizes[i].getQuizName()==key]
            answers=[]
            trueAnswers=[x.getQuestion().getAnswer() for x in  self.__pollList[key][0].getQuizes()[i].getQuizParts()
                         if self.__pollList[key][0].getQuizes[i].getQuizName()==key]

            stuList = self.__pollList[key]
            for index,stu in enumerate(stuList):

                num = len(self.__pollList[key][0].getQuizes()[i].getQuizParts())

                for j in range(num):
                    a_dict={}
                    q = self.__pollList[key][0].getQuizes()[i].getQuizParts()[j].getQuestion().getQuestionText()


                    respond=stu.getQuizes()[i].getQuizParts()[j].getStudentRespond()

                    for r in respond:

                        if not r in a_dict:
                            a_dict[r]=1
                        else:
                            a_dict[r]=a_dict[r]+1
                    answers.append(a_dict)
            i+=1
            self.__quizQuestStat[key]=[questions,answers,trueAnswers]
        a=5


    def getStuIndexWithUserName(self, username):

        for stu in self.__studentList:
            y = stu.getName() + " " + stu.getSurname()

            if y.lower() == username.lower():
                return self.__studentList.index(stu)

    def printStudentList(self):
        print(*self.__studentList, sep='\n')

    def extractPollList(self):

        for stu in self.__studentList:
            for quiz in stu.getQuizes():
                if not quiz.getQuizName() in self.__pollList:

                    self.__pollList[quiz.getQuizName()]=[]
                    x= self.__pollList[quiz.getQuizName()]
                    x.append(stu)
                else:
                    x=self.__pollList[quiz.getQuizName()]
                    if not stu in x:
                        x.append(stu)

    def calculateQuizStats(self):

        for stu in self.__studentList:
            for quiz in stu.getQuizes():
                if not quiz.getQuizName() in self.__pollList:

                    self.__pollList[quiz.getQuizName()] = QuizStat(quiz.getNumOfQuestions())


                self.__pollList[quiz.getQuizName()].attendingStuList.append(stu)

                qzStat=self.__pollList[quiz.getQuizName()]
                qStatDict=qzStat.questionStatDict


                for quizPart in quiz.getQuizParts():

                    stu.numTotalQuestionSolved+=1

                    if quizPart not in qzStat.quizParts:
                        qzStat.quizParts.append(quizPart)

                    if quizPart not in qStatDict:
                        qStatDict[quizPart]=QuestionStat()

                    if quizPart.getIsCorrect()==1:
                        stu.numTotalCorrect+=1
                        qStatDict[quizPart].addCorrectResp(stu)

                    elif quizPart.getIsCorrect()==0:
                        qStatDict[quizPart].addWrongResp(stu)
                        stu.numTotalWrong+=1

                    qStatDict[quizPart].question=quizPart.getQuestion()

                    astat=qStatDict[quizPart].answerStat

                    astat.setCorrectAnswer(quizPart.getQuestion().getAnswer())

                    for r in quizPart.getStudentRespond():

                       astat.addAnswer(r,stu,qStatDict[quizPart].numTotalResponders)