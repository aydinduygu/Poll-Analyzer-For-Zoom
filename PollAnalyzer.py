from OutputProducer import OutputProducer
from Parser import Parser
import glob, os
from StringComparator import StringComparator


class PollAnalyzer:
    __studentList = None
    __fileNames = None
    __answerKeys=None
    __attendanceData = None
    __myOutputProducer = None
    __pollList=None
    __quizQuestStat=None

    def __init__(self):

        self.__studentList=[]
        self.__fileNames=[]
        self.__attendanceData=[]
        self.__answerKeys=[]
        self.__myOutputProducer = OutputProducer.instance()
        self.__myOutputProducer.addIntoExecutionLog("System started!")
        self.__pollList={}
        self.__quizQuestStat={}

        path="./poll_files/"
        path2="./poll_answers/"

        for file in glob.glob(path+"*.csv"):
            self.__fileNames.append(file)

        for file in glob.glob("*.xls"):
            if file != "studentList.XLS":
                self.__fileNames.append(file)

        for file in glob.glob(path2+"*.xls"):
            self.__answerKeys.append(file)

        filePath = "./poll_files/studentList.XLS"
        #self.__studentList = parser.parseStudentList(filePath, "Adı", "Soyadı", "Öğrenci No")

        columnNames={"name":"Adı","surname":"Soyadı","id":"Öğrenci No","username":"User Name","email":"User Email","datetime":"Submitted Date/Time"}

        parser = Parser(filePath,self.__fileNames,self.__answerKeys,columnNames)
        self.__studentList=parser.getStudentList()

        self.calculateQuizResults()

        self.extractPollList()

        self.calcQuestionStat()

        self.__myOutputProducer.printPollStatictics(self.__quizQuestStat)
        self.__myOutputProducer.printAttendenceReport(self.__studentList)
        self.__myOutputProducer.printPollResults(self.__studentList,self.__pollList)



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

    def calculateQuizResults(self):

        for student in self.__studentList:

            for quiz in student.getQuizes():

                for quizPart in quiz.getQuizParts():

                    match=0

                    for r in quizPart.getStudentRespond():

                        for a in quizPart.getQuestion().getAnswer():

                            match = StringComparator(a,r).cmp_ig_C_S_P_N
                            if match==0:
                                break
                        if match!=0:
                            break

                    if match==0:
                        quizPart.setIsCorrect(1)
                        quiz.setNumCorrect(quiz.getNumCorrect()+1)
                    else:
                        quizPart.setIsCorrect(0)
                        quiz.setNumWrong(quiz.getNumWrong()+1)


    def calcQuestionStat(self):

        i=0
        for key in self.__pollList:

                num=len(self.__pollList[key][0].getQuizes()[i].getQuizParts())

                questions=[x.getQuestion().getQuestionText() for x in self.__pollList[key][0].getQuizes()[i].getQuizParts()]
                answers=[]
                trueAnswers=[x.getQuestion().getAnswer() for x in  self.__pollList[key][0].getQuizes()[i].getQuizParts()]
                for j in range(num):
                    a_dict={}
                    q = self.__pollList[key][0].getQuizes()[i].getQuizParts()[j].getQuestion().getQuestionText()

                    stuList=self.__pollList[key]
                    for stu in stuList:
                        respond=stu.getQuizes()[i].getQuizParts()[j].getStudentRespond()


                        for r in respond:

                            if not r in a_dict:
                                a_dict[r]=1
                            else:
                                a_dict[r]=a_dict[r]+1
                    answers.append(a_dict)

                self.__quizQuestStat[key]=[questions,answers,trueAnswers]

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
