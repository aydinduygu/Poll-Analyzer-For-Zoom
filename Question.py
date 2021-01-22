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

    def getQuestionText(self):
        return self.__questionText

    def getAnswer(self):
        return self.__answer

    def setAnswer(self, answer):
        self.__answer = answer

    def __str__(self):
        return self.__questionText