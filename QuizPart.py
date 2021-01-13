from Question import Question


class QuizPart:
    __question = None
    __studentRespond = None

    def __init__(self, question, studentRespond):
        self.__question = question
        self.__studentRespond = studentRespond

    def getQuestion(self):
       return self.__question

    def getStudentRespond(self):
        return self.__studentRespond