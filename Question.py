class Question:
    __questionId = None
    __questionText = None
    __answer = None

    def __init__(self, questionId, questionText, answer):
        self.__questionId = questionId
        self.__questionText = questionText
        self.__answer = answer
