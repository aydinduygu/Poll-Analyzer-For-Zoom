from QuizPart import QuizPart
from StringComparator import StringComparator

class Quiz:

    __quizName=None
    __quizParts = None
    __quizDate=None
    __numCorrect=None
    __numWrong=None
    __topic=None

    def __init__(self, quizParts,quizDate):
        self.__quizParts = quizParts
        self.__numWrong=0
        self.__numCorrect=0
        self.__quizDate=quizDate
        self.__numberOfQuestions=0
        self.__topic=""

    def getQuizParts(self):
        return self.__quizParts

    def setQuizParts(self,qpList):
        self.__quizParts=qpList
        self.__numberOfQuestions=len(qpList)

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

    def __str__(self):
        return self.__quizName

    def getNumOfQuestions(self):
        return self.__numberOfQuestions

    def setNumOfQuestions(self, num):
        self.__numberOfQuestions=num

    def __hash__(self):
        return hash(self.__quizName)

    def __eq__(self, other):

        if isinstance(other,str):
            cmpstr = StringComparator(self.__quizName(), other).cmp_ig_CaseSpacePunc

        elif isinstance(other,Quiz):

            return self.__quizName==other.getQuizName()

        else:
            return False

    def __lt__(self, other):

        if isinstance(other, str):
            cmpstr = StringComparator(self.__quizName(), other).cmp_ig_CaseSpacePunc

        elif isinstance(other, Quiz):

            cmpstr = StringComparator(self.__quizName(), other.getQuizName()).cmp_ig_CaseSpacePunc

            if cmpstr == -1:
                return True
            else:
                return False

    def __gt__(self, other):

        if isinstance(other, str):
            cmpstr = StringComparator(self.__quizName(), other).cmp_ig_CaseSpacePunc

        elif isinstance(other, Quiz):

            cmpstr = StringComparator(self.__quizName(), other.getQuizName()).cmp_ig_CaseSpacePunc

            if cmpstr == 1:
                return True
            else:
                return False
