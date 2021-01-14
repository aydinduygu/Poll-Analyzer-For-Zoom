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

    def __eq__(self, other):
        if other.getStudentId()==self.__studentId:
            return True
        else: return False

    def __str__(self):
        return self.__studentId+" "+self.__name+" "+self.__surname

    def getStudentId(self):
        return self.__studentId

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname

    def increaseAttendance(self):
        self.__attendance=self.__attendance+1


