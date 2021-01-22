from QuizPart import QuizPart


class Quiz:

    __quizName=None
    __quizParts = None
    __quizDate=None
    __numCorrect=None
    __numWrong=None

    def __init__(self, quizParts,quizDate):
        self.__quizParts = quizParts
        self.__numWrong=0
        self.__numCorrect=0
        self.__quizDate=quizDate


    def getQuizParts(self):
        return self.__quizParts

    def getNumCorrect(self):
        return self.__numCorrect

    def getNumWrong(self):
        return self.__numWrong


    def getQuizName(self):
        return self.__quizName

    def setQuizName(self,name):
        self.__quizName=name


    def setNumWrong(self,num):
        self.__numWrong=num

    def setNumCorrect(self,num):
        self.__numCorrect=num

