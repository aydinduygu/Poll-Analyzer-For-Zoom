from Quiz import Quiz
from Attendence import Attendence


class Student:
    __name = None
    __surname = None
    __username=None
    __studentId = None
    __attendence=None
    __quizes=None
    __email=None



    def __init__(self, name, surname, studentId):
        self.__name = name
        self.__surname = surname
        self.__studentId = studentId
        self.__quizes=[]
        self.__attendence=Attendence()

    def __str__(self):
        return self.__studentId + " " + self.__name + " " + self.__surname

    def getStudentId(self):
        return self.__studentId

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname

    def getQuizes(self):
        return self.__quizes

    def as_dict(self):
        return {'Student Id':self.__studentId,'Name':self.__name,'Surname':self.__surname}

    def getAttendence(self):
        return self.__attendence

    def setAttendence(self,attendence:Attendence):
        self.__attendence=attendence

    def getUsername(self):
        return self.__username

    def setUsername(self,username:str):
        self.__username=username


    def setEmail(self,email):
        self.__email=email

    def getEmail(self):
        return self.__email