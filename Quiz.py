from QuizPart import QuizPart


class Quiz:
    __quizParts = None
    __numCorrect=None
    __numWrong=None

    def __init__(self, quizParts):
        self.__quizParts = quizParts
        self.__numWrong=0
        self.__numCorrect=0

    def getQuizParts(self):
        return self.__quizParts

    def getNumCorrect(self):
        return self.__numCorrect

    def getNumWrong(self):
        return self.__numWrong