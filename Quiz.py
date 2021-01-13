from QuizPart import QuizPart


class Quiz:
    __quizParts = []

    def __init__(self, quizParts):
        self.__quizParts = quizParts

    def getQuizParts(self):
        return self.__quizParts