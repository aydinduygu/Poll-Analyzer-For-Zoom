from Quiz import Quiz

class Student:
    __name = ""
    __surname = ""
    __studentId = 0
    __attendance = 0

    def __init__(self, name, surname, studentId):
        self.__name = name
        self.__surname = surname
        self.__studentId = studentId
