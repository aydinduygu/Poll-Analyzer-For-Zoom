from Quiz import Quiz


class Student:
    __name = None
    __surname = None
    __studentId = None
    __attendance = None
    __quizes=None
    __numberOfClasses=0


    def __init__(self, name, surname, studentId):
        self.__name = name
        self.__surname = surname
        self.__studentId = studentId
        self.__attendance=0
        self.__quizes=[]



    def __str__(self):
        return self.__studentId + " " + self.__name + " " + self.__surname


    def getStudentId(self):
        return self.__studentId

    def getName(self):
        return self.__name

    def getSurname(self):
        return self.__surname

    def increaseAttendance(self):

        if self.__attendance==None:
            self.__attendance=0
        self.__attendance = self.__attendance + 1

    def getQuizes(self):
        return self.__quizes

    def getNumClasses(self):
        return self.__numberOfClasses

    def setNumClasses(self, num):
        self.__numberOfClasses=num


    def as_dict(self):
        return {'Student Id':self.__studentId,'Name':self.__name,'Surname':self.__surname}

    def getAttendence(self):
        return self.__attendance

    def getNumberOfClasses(self):
        return self.__numberOfClasses