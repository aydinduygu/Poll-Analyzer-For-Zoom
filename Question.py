from StringComparator import StringComparator

class Question:
    __questionNumber = None
    __questionText = None
    __answer = None

    def __init__(self, questionNumber, questionText, answer):
        self.__questionNumber = questionNumber
        self.__questionText = questionText
        self.__answer = answer

    def getQuestionNumber(self):
        return self.__questionNumber

    def setQuestionNumber(self,num):
        self.__questionNumber=num

    def getQuestionText(self):
        return self.__questionText

    def getAnswer(self):
        return self.__answer

    def setAnswer(self, answer):
        self.__answer = answer

    def __str__(self):
        return self.__questionText

    def __eq__(self, other):

        if not isinstance(other,Question):
            return False
        cmpstr=StringComparator(self.getQuestionText(),other.getQuestionText()).cmp_ig_CaseSpacePunc

        if cmpstr==0:
            return True
        else:
            return False

    def __lt__(self, other):

        cmpstr=StringComparator(self.getQuestionText(),other.getQuestionText()).cmp_ig_CaseSpacePunc

        if cmpstr==-1:
            return True
        else:
            return False

    def __gt__(self, other):

        cmpstr=StringComparator(self.getQuestionText(),other.getQuestionText()).cmp_ig_CaseSpacePunc

        if cmpstr==1:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.getQuestionText()))