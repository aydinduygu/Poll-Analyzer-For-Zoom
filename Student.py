from Quiz import Quiz
from StringComparator import StringComparator
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
        self.numAttendedQuizes=0
        self.numTotalCorrect=0
        self.numTotalWrong=0
        self.numTotalQuestionSolved=0

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

    def __lt__(self, other):
        name1=self.getName()+" "+self.getSurname()
        name2=other.getName()+" "+other.getSurname()

        strcmp=StringComparator(name1,name2)
        if strcmp.cmp_ig_C_S_P_N==-1:
            return True
        else:
            return False

    def __gt__(self, other):
        name1 = self.getName() + " " + self.getSurname()
        name2 = other.getName() + " " + other.getSurname()

        strcmp = StringComparator(name1, name2)
        if strcmp.cmp_ig_C_S_P_N == 1:
            return True
        else:
            return False

    def __eq__(self, other):
        name1 = self.getName() + " " + self.getSurname()
        name2 = other.getName() + " " + other.getSurname()

        strcmp = StringComparator(name1, name2)
        if strcmp.cmp_ig_C_S_P_N == 0:
            return True
        else:
            return False