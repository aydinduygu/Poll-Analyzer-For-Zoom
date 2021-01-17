from QuizPart import QuizPart


class Quiz:
    __quizParts = []
    __numCorrect=0
    __numWrong=0

    def __init__(self, quizParts):
        self.__quizParts = quizParts

    def getQuizParts(self):
        return self.__quizParts